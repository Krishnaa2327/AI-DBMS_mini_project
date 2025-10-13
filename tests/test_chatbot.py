#!/usr/bin/env python3
"""
Test script for Medical Chatbot
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from chatbot import MedicalChatbot

def test_chatbot_flow():
    """Test a complete chatbot conversation flow."""
    print("=" * 60)
    print("MEDICAL CHATBOT TEST")
    print("=" * 60)
    
    bot = MedicalChatbot()
    
    # Start conversation
    print("\n1. Starting conversation...")
    response = bot.start_conversation()
    print(f"Bot: {response[:100]}...")
    assert bot.conversation_state == "patient_info"
    print("✅ Conversation started successfully!")
    
    # Provide patient info
    print("\n2. Providing patient information...")
    response = bot.process_message("John Smith, 35, Male")
    print(f"Bot: {response[:100]}...")
    assert bot.conversation_state == "primary_symptom"
    assert bot.patient_info['name'] == 'John Smith'
    print("✅ Patient info processed successfully!")
    
    # Describe primary symptoms
    print("\n3. Describing primary symptoms...")
    response = bot.process_message("I have a bad headache and I'm feeling very tired")
    print(f"Bot: {response[:150]}...")
    assert 'headache' in bot.collected_symptoms
    assert 'fatigue' in bot.collected_symptoms
    print("✅ Symptoms identified successfully!")
    
    # Answer follow-up questions
    print("\n4. Answering follow-up questions...")
    
    # The bot asks "Do you have fever?" after identifying initial symptoms
    # We need to answer yes/no for remaining symptoms until we reach 8 total or run out
    # Already have: headache, fatigue (2 symptoms)
    # Will ask about: fever and 5 more to reach 8 total, or until all asked
    
    # Answer questions (up to 8 symptoms total)
    for i in range(10):  # Max iterations to be safe
        response = bot.process_message("yes" if i < 3 else "no")  # Answer yes for first 3, no for rest
        if bot.conversation_state == "medical_history":
            break
        if i > 0 and i % 2 == 0:
            print(f"  Answered {i} follow-up questions...")
    
    print(f"Final state: {bot.conversation_state}")
    assert bot.conversation_state == "medical_history"
    print("✅ Symptom questions completed!")
    
    # Answer medical history
    print("\n5. Answering medical history questions...")
    response = bot.process_message("no")  # diabetes
    response = bot.process_message("no")  # hypertension
    response = bot.process_message("no")  # smoker
    
    print(f"Bot: {response[:100]}...")
    assert bot.conversation_state == "vital_signs_optional"
    print("✅ Medical history completed!")
    
    # Skip vital signs and get prediction
    print("\n6. Generating prediction...")
    response = bot.process_message("no")
    
    print(f"\nBot Response:\n{response}")
    
    assert "AI Prediction Results" in response
    assert bot.conversation_state == "completed"
    print("\n✅ Prediction generated successfully!")
    
    # Check collected data
    print("\n7. Checking collected data...")
    data = bot.get_collected_data()
    print(f"Patient: {data['patient_info']}")
    print(f"Symptoms collected: {sum(1 for v in data['symptoms'].values() if v == 1)}")
    print("✅ Data collection verified!")
    
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED! ✅")
    print("=" * 60)

def test_symptom_identification():
    """Test symptom identification from text."""
    print("\n\nTesting symptom identification...")
    bot = MedicalChatbot()
    
    test_cases = [
        ("I have a fever and cough", ["fever", "cough"]),
        ("my throat is sore and I feel tired", ["sore_throat", "fatigue"]),
        ("I'm vomiting and have diarrhea", ["vomiting", "diarrhea"]),
        ("I can't breathe well", ["shortness_of_breath"]),
    ]
    
    for text, expected in test_cases:
        identified = bot._identify_symptoms(text)
        print(f"Text: '{text}'")
        print(f"Expected: {expected}")
        print(f"Identified: {identified}")
        assert all(symptom in identified for symptom in expected), f"Failed for: {text}"
        print("✅ Passed\n")
    
    print("All symptom identification tests passed! ✅")

if __name__ == "__main__":
    try:
        test_symptom_identification()
        print("\n")
        test_chatbot_flow()
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
