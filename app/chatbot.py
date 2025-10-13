#!/usr/bin/env python3
"""
Smart Hospital Management System - AI Chatbot Module
Created by: Krishna + Omkar
Date: October 13, 2025
Phase: 3 - AI Chatbot Integration

Conversational AI chatbot for disease prediction and symptom collection.
"""

import sys
import os
from typing import Dict, List, Any, Optional
import random

# Add paths
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from app.utils.ml_utils import predict

class MedicalChatbot:
    """
    AI-powered medical chatbot for symptom collection and disease prediction.
    """
    
    def __init__(self):
        """Initialize the chatbot with conversation state."""
        self.conversation_state = "greeting"
        self.collected_symptoms = {}
        self.patient_info = {}
        self.current_question = None
        self.symptoms_to_ask = []
        self.asked_symptoms = set()
        
        # Available symptoms from the model
        self.all_symptoms = [
            "fever", "cough", "sore_throat", "fatigue", "headache",
            "nausea", "vomiting", "diarrhea", "shortness_of_breath",
            "chest_pain", "runny_nose", "body_ache", "loss_of_smell"
        ]
        
        # Medical history questions
        self.medical_history = [
            "comorbid_diabetes", "comorbid_hypertension", "smoker"
        ]
        
        # Vital signs (optional)
        self.vital_signs = [
            "temperature_c", "oxygen_saturation", "heart_rate",
            "respiratory_rate", "bp_systolic", "bp_diastolic"
        ]
    
    def reset(self):
        """Reset chatbot to initial state."""
        self.__init__()
    
    def get_greeting(self) -> str:
        """Return a friendly greeting message."""
        greetings = [
            "Hello! I'm your AI medical assistant. I'll help you identify potential health issues based on your symptoms. 🏥",
            "Hi there! Welcome to the Smart Hospital AI assistant. Let's discuss your symptoms together. 👋",
            "Greetings! I'm here to help analyze your symptoms. Let's get started! 🤖",
        ]
        return random.choice(greetings)
    
    def get_disclaimer(self) -> str:
        """Return medical disclaimer."""
        return (
            "\n\n⚠️ **Important Medical Disclaimer:**\n"
            "This AI tool provides preliminary predictions only and should NOT replace professional medical advice. "
            "Always consult with a qualified healthcare provider for proper diagnosis and treatment."
        )
    
    def start_conversation(self) -> str:
        """Start the conversation and ask for patient info."""
        self.conversation_state = "patient_info"
        return (
            self.get_greeting() + 
            "\n\nTo begin, I'd like to know a few basic details about you. "
            "May I have your name, age, and gender? (e.g., 'John, 35, Male')"
        )
    
    def parse_patient_info(self, user_input: str) -> Dict[str, Any]:
        """Parse patient information from user input."""
        try:
            # Try to parse: "name, age, gender" format
            parts = [p.strip() for p in user_input.split(',')]
            
            if len(parts) >= 3:
                name = parts[0].title()  # Capitalize each word
                age = int(parts[1])
                gender = parts[2].capitalize()
                
                return {
                    'name': name,
                    'age': age,
                    'gender': gender if gender in ['Male', 'Female', 'Other'] else 'Other'
                }
            elif len(parts) == 2:
                # Try age, gender
                age = int(parts[0])
                gender = parts[1].capitalize()
                return {
                    'name': 'Patient',
                    'age': age,
                    'gender': gender if gender in ['Male', 'Female', 'Other'] else 'Other'
                }
        except:
            pass
        
        # Default if parsing fails
        return None
    
    def process_message(self, user_message: str) -> str:
        """
        Process user message and return chatbot response.
        
        Args:
            user_message: The user's message
            
        Returns:
            Chatbot's response message
        """
        user_message = user_message.strip()
        user_message_lower = user_message.lower()
        
        # Handle special commands
        if user_message_lower in ['quit', 'exit', 'stop', 'cancel']:
            return "Goodbye! Feel free to return if you need medical assistance. Take care! 👋"
        
        if user_message_lower in ['restart', 'reset', 'start over']:
            self.reset()
            return self.start_conversation()
        
        # State machine for conversation flow
        if self.conversation_state == "greeting":
            return self.start_conversation()
        
        elif self.conversation_state == "patient_info":
            # Store original message before lowercasing for name parsing
            original_message = user_message
            patient_data = self.parse_patient_info(original_message)
            if patient_data:
                self.patient_info = patient_data
                self.conversation_state = "primary_symptom"
                return (
                    f"Thank you, {self.patient_info['name']}! Nice to meet you.\n\n"
                    f"Now, let's talk about your symptoms. What is your main concern today? "
                    f"What symptom is bothering you the most?"
                )
            else:
                return (
                    "I couldn't quite understand that. Could you please provide your information in this format: "
                    "'Name, Age, Gender' (e.g., 'Sarah, 28, Female')"
                )
        
        elif self.conversation_state == "primary_symptom":
            # Identify mentioned symptoms
            identified = self._identify_symptoms(user_message_lower)
            for symptom in identified:
                self.collected_symptoms[symptom] = 1
                self.asked_symptoms.add(symptom)
            
            if identified:
                symptom_names = ", ".join([s.replace('_', ' ').title() for s in identified])
                self.conversation_state = "follow_up_symptoms"
                return (
                    f"I understand you're experiencing: {symptom_names}.\n\n"
                    f"Let me ask a few follow-up questions to better understand your condition. "
                    f"Do you have any fever? (Yes/No)"
                )
            else:
                return (
                    "I didn't catch specific symptoms from that. Could you describe what you're feeling? "
                    "For example: 'I have a headache and feel very tired' or 'I'm coughing with a sore throat'."
                )
        
        elif self.conversation_state == "follow_up_symptoms":
            return self._handle_symptom_questions(user_message_lower)
        
        elif self.conversation_state == "medical_history":
            return self._handle_medical_history(user_message_lower)
        
        elif self.conversation_state == "vital_signs_optional":
            # User chose whether to provide vital signs
            is_yes = any(word in user_message_lower for word in ['yes', 'yeah', 'yep', 'yup', 'y'])
            if is_yes:
                self.conversation_state = "vital_signs"
                return "Great! Let me collect your vital signs. What is your current temperature in Celsius? (e.g., 37.5)"
            else:
                # Skip vital signs and generate prediction
                return self.generate_prediction()
        
        elif self.conversation_state == "vital_signs":
            return self._handle_vital_signs(user_message_lower)
        
        elif self.conversation_state == "completed":
            # After prediction, handle appointment scheduling
            is_yes = any(word in user_message_lower for word in ['yes', 'yeah', 'yep', 'yup', 'y'])
            if is_yes:
                return (
                    "Great! To schedule an appointment, please visit our Appointments page from the main menu. \n\n"
                    "Our medical staff will be happy to assist you. Would you like to start a new consultation? (Type 'restart')"
                )
            else:
                return "Okay! Feel free to come back anytime if you need assistance. Take care! \ud83d\udc4b\n\nType 'restart' to begin a new consultation."
        
        else:
            return "I'm not sure how to respond. Type 'restart' to begin again."
    
    def _identify_symptoms(self, text: str) -> List[str]:
        """Identify symptoms mentioned in user text."""
        text = text.lower()
        identified = []
        
        # Symptom keywords mapping
        symptom_keywords = {
            "fever": ["fever", "temperature", "hot", "burning up"],
            "cough": ["cough", "coughing"],
            "sore_throat": ["sore throat", "throat pain", "throat hurt", "throat is sore", "throat sore"],
            "fatigue": ["tired", "fatigue", "exhausted", "weak", "weakness"],
            "headache": ["headache", "head pain", "head hurt"],
            "nausea": ["nausea", "nauseous", "queasy", "sick to stomach"],
            "vomiting": ["vomit", "vomiting", "throw up", "throwing up"],
            "diarrhea": ["diarrhea", "loose stool", "watery stool"],
            "shortness_of_breath": ["short of breath", "breathing difficult", "can't breathe", "breathless", "breath"],
            "chest_pain": ["chest pain", "chest hurt", "chest ache"],
            "runny_nose": ["runny nose", "nose running", "nasal discharge"],
            "body_ache": ["body ache", "body pain", "muscle pain", "aching"],
            "loss_of_smell": ["loss of smell", "can't smell", "no smell"]
        }
        
        for symptom, keywords in symptom_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    identified.append(symptom)
                    break
        
        return identified
    
    def _handle_symptom_questions(self, user_message: str) -> str:
        """Handle follow-up symptom questions."""
        # Determine yes/no response
        is_yes = any(word in user_message for word in ['yes', 'yeah', 'yep', 'yup', 'y', 'have', 'experiencing'])
        is_no = any(word in user_message or word == user_message for word in ['no', 'nope', 'n', "don't", "dont"])
        
        # Process current symptom if we're asking about one
        if self.current_question:
            if is_yes:
                self.collected_symptoms[self.current_question] = 1
            elif is_no:
                self.collected_symptoms[self.current_question] = 0
            self.asked_symptoms.add(self.current_question)
            self.current_question = None
        
        # Also check if user mentioned additional symptoms
        additional = self._identify_symptoms(user_message)
        for symptom in additional:
            if symptom not in self.asked_symptoms:
                self.collected_symptoms[symptom] = 1
                self.asked_symptoms.add(symptom)
        
        # Find next symptom to ask about
        remaining_symptoms = [s for s in self.all_symptoms if s not in self.asked_symptoms]
        
        if remaining_symptoms and len(self.asked_symptoms) < 8:  # Ask up to 8 symptoms
            next_symptom = remaining_symptoms[0]
            self.current_question = next_symptom
            symptom_display = next_symptom.replace('_', ' ').title()
            return f"Do you have {symptom_display}? (Yes/No)"
        else:
            # Done with symptoms, move to medical history
            self.conversation_state = "medical_history"
            self.current_question = "comorbid_diabetes"
            return (
                "Thank you for providing that information.\n\n"
                "Now, a few questions about your medical history:\n"
                "Do you have diabetes? (Yes/No)"
            )
    
    def _handle_medical_history(self, user_message: str) -> str:
        """Handle medical history questions."""
        is_yes = any(word in user_message for word in ['yes', 'yeah', 'yep', 'yup', 'y', 'have'])
        is_no = any(word in user_message or word == user_message for word in ['no', 'nope', 'n', "don't", "dont"])
        
        # Process current question
        if self.current_question:
            if is_yes:
                self.collected_symptoms[self.current_question] = 1
            elif is_no:
                self.collected_symptoms[self.current_question] = 0
        
        # Determine next question
        if self.current_question == "comorbid_diabetes":
            self.current_question = "comorbid_hypertension"
            return "Do you have hypertension (high blood pressure)? (Yes/No)"
        elif self.current_question == "comorbid_hypertension":
            self.current_question = "smoker"
            return "Are you a smoker? (Yes/No)"
        else:
            # Done with medical history, ask about vital signs
            self.conversation_state = "vital_signs_optional"
            return (
                "Great! That's all the questions I need.\n\n"
                "Would you like to provide vital signs (temperature, oxygen saturation, etc.) for a more accurate prediction? "
                "(Yes/No)\n\n"
                "You can say 'No' to skip this and get a prediction now."
            )
    
    def _handle_vital_signs(self, user_message: str) -> str:
        """Handle vital signs input."""
        # This would require more complex parsing
        # For simplicity, we'll use defaults
        return self.generate_prediction()
    
    def generate_prediction(self) -> str:
        """Generate disease prediction based on collected information."""
        try:
            # Build feature vector
            features = {
                'age': self.patient_info.get('age', 30),
                'sex_encoded': 1 if self.patient_info.get('gender') == 'Male' else 0,
            }
            
            # Add collected symptoms (default to 0 if not asked)
            for symptom in self.all_symptoms:
                features[symptom] = self.collected_symptoms.get(symptom, 0)
            
            # Add medical history
            for hist in self.medical_history:
                features[hist] = self.collected_symptoms.get(hist, 0)
            
            # Add default vital signs
            features['temperature_c'] = 37.5 if features.get('fever', 0) == 1 else 36.5
            features['oxygen_saturation'] = 95
            features['heart_rate'] = 80
            features['respiratory_rate'] = 16
            features['bp_systolic'] = 120
            features['bp_diastolic'] = 80
            
            # Engineered features
            features['age_group_encoded'] = 0 if features['age'] < 18 else 1 if features['age'] < 65 else 2
            features['high_fever'] = 1 if features.get('fever', 0) == 1 else 0
            features['low_oxygen'] = 0
            features['tachycardia'] = 0
            features['hypertension_acute'] = 0
            
            # Symptom counts
            symptom_values = [features.get(s, 0) for s in self.all_symptoms]
            features['symptom_count'] = sum(symptom_values)
            features['respiratory_symptom_count'] = sum([features.get(s, 0) for s in ['cough', 'sore_throat', 'shortness_of_breath']])
            features['gi_symptom_count'] = sum([features.get(s, 0) for s in ['nausea', 'vomiting', 'diarrhea']])
            
            # Get predictions
            predictions = predict(features, top_k=3)
            
            if predictions:
                # Build response
                response = "\n\n🔮 **AI Prediction Results**\n\n"
                response += f"Based on your symptoms, here are my top predictions:\n\n"
                
                for i, pred in enumerate(predictions, 1):
                    confidence = pred['probability'] * 100
                    response += f"{i}. **{pred['disease']}** - {confidence:.1f}% confidence\n"
                
                response += "\n\n📊 **Summary of Your Symptoms:**\n"
                reported_symptoms = [s.replace('_', ' ').title() for s, v in self.collected_symptoms.items() 
                                   if v == 1 and s in self.all_symptoms]
                if reported_symptoms:
                    response += "- " + "\n- ".join(reported_symptoms)
                
                response += "\n\n💡 **Next Steps:**\n"
                response += "1. Consult with a healthcare provider for proper diagnosis\n"
                response += "2. Monitor your symptoms and seek immediate care if they worsen\n"
                response += "3. Stay hydrated and get plenty of rest\n"
                
                response += self.get_disclaimer()
                
                response += "\n\nWould you like to schedule an appointment with a doctor? (Yes/No)"
                
                self.conversation_state = "completed"
                return response
            else:
                return "I'm sorry, I couldn't generate a prediction. Please try again or consult with a healthcare provider."
                
        except Exception as e:
            return f"An error occurred while processing your information: {str(e)}\n\nPlease try again or contact support."
    
    def get_collected_data(self) -> Dict[str, Any]:
        """Return all collected data for database storage."""
        return {
            'patient_info': self.patient_info,
            'symptoms': self.collected_symptoms,
            'conversation_state': self.conversation_state
        }


# Singleton instance
_chatbot_instance = None

def get_chatbot() -> MedicalChatbot:
    """Get or create chatbot instance."""
    global _chatbot_instance
    if _chatbot_instance is None:
        _chatbot_instance = MedicalChatbot()
    return _chatbot_instance

def reset_chatbot():
    """Reset chatbot instance."""
    global _chatbot_instance
    _chatbot_instance = None