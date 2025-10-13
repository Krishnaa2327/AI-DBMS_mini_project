# AI Medical Chatbot - Documentation

## Overview

The AI Medical Chatbot is an intelligent conversational assistant integrated into the Smart Hospital Management System. It provides a natural, conversation-based approach to collecting patient symptoms and generating disease predictions using the trained Random Forest ML model.

## Features

### 🎯 Core Capabilities

1. **Conversational Symptom Collection**
   - Natural language understanding
   - Smart symptom identification from free-text descriptions
   - Follow-up questions for comprehensive assessment

2. **Intelligent Disease Prediction**
   - Integration with Random Forest ML model (48% accuracy)
   - Top 3 disease predictions with confidence scores
   - Symptom summarization

3. **Medical History Collection**
   - Diabetes status
   - Hypertension status
   - Smoking history

4. **Session Management**
   - Persistent chat history within session
   - New chat functionality
   - Conversation state tracking

5. **Database Integration**
   - Automatic patient creation/lookup
   - Prediction results saved to medical records
   - Seamless integration with existing patient database

## Architecture

### Components

```
app/
├── chatbot.py              # Core chatbot logic and conversation management
├── main.py                 # Streamlit UI with chatbot page integration
├── test_chatbot.py         # Comprehensive test suite
└── utils/
    └── ml_utils.py         # ML model integration
```

### Conversation Flow

```
1. Greeting → 2. Patient Info → 3. Primary Symptom → 4. Follow-up Questions → 
5. Medical History → 6. Vital Signs (Optional) → 7. Prediction → 8. Appointment Offer
```

### State Machine

- **greeting**: Initial state
- **patient_info**: Collecting name, age, gender
- **primary_symptom**: User describes main concern
- **follow_up_symptoms**: Bot asks yes/no questions about specific symptoms
- **medical_history**: Collecting comorbidities and risk factors
- **vital_signs_optional**: Asking if user wants to provide vital signs
- **vital_signs**: Collecting temperature, oxygen saturation, etc.
- **completed**: Prediction generated, offer appointment scheduling

## Usage

### Starting the Chatbot

1. Run the Streamlit app:
   ```bash
   streamlit run app/main.py
   ```

2. Navigate to **💬 AI Chatbot** from the sidebar menu

3. The chatbot will greet you and start the conversation

### Example Conversation

```
🤖 Bot: Hello! I'm your AI medical assistant. I'll help you identify potential 
        health issues based on your symptoms. 🏥
        
        To begin, I'd like to know a few basic details about you. 
        May I have your name, age, and gender? (e.g., 'John, 35, Male')

👤 User: Sarah, 28, Female

🤖 Bot: Thank you, Sarah! Nice to meet you.
        
        Now, let's talk about your symptoms. What is your main concern today? 
        What symptom is bothering you the most?

👤 User: I have a terrible headache and I'm feeling very tired

🤖 Bot: I understand you're experiencing: Headache, Fatigue.
        
        Let me ask a few follow-up questions to better understand your condition. 
        Do you have any fever? (Yes/No)

👤 User: Yes

🤖 Bot: Do you have Cough? (Yes/No)

👤 User: No

... [continues with more symptom questions] ...

🤖 Bot: 🔮 **AI Prediction Results**
        
        Based on your symptoms, here are my top predictions:
        
        1. **Common Cold** - 42.5% confidence
        2. **Migraine** - 28.3% confidence
        3. **COVID-19** - 15.7% confidence
        
        📊 **Summary of Your Symptoms:**
        - Headache
        - Fatigue
        - Fever
        
        💡 **Next Steps:**
        1. Consult with a healthcare provider for proper diagnosis
        2. Monitor your symptoms and seek immediate care if they worsen
        3. Stay hydrated and get plenty of rest
        
        ⚠️ **Important Medical Disclaimer:**
        This AI tool provides preliminary predictions only and should NOT replace 
        professional medical advice. Always consult with a qualified healthcare 
        provider for proper diagnosis and treatment.
        
        Would you like to schedule an appointment with a doctor? (Yes/No)
```

### Chat Commands

- **restart** / **reset** / **start over**: Begin a new conversation
- **quit** / **exit** / **stop** / **cancel**: End the conversation

## Technical Details

### Symptom Recognition

The chatbot can identify 13 symptoms from natural language:
- Fever
- Cough
- Sore throat
- Fatigue
- Headache
- Nausea
- Vomiting
- Diarrhea
- Shortness of breath
- Chest pain
- Runny nose
- Body ache
- Loss of smell

### Keyword Mapping Examples

| User Input | Identified Symptom |
|------------|-------------------|
| "I have a fever" | fever |
| "my throat is sore" | sore_throat |
| "feeling very tired" | fatigue |
| "I can't breathe well" | shortness_of_breath |
| "throwing up" | vomiting |

### ML Model Integration

The chatbot builds a complete 31-feature vector for the Random Forest model:

**Demographics (2 features):**
- age
- sex_encoded

**Medical History (3 features):**
- comorbid_diabetes
- comorbid_hypertension
- smoker

**Vital Signs (6 features):**
- temperature_c
- oxygen_saturation
- heart_rate
- respiratory_rate
- bp_systolic
- bp_diastolic

**Symptoms (13 features):**
- All 13 symptoms listed above

**Engineered Features (8 features):**
- age_group_encoded
- high_fever
- low_oxygen
- tachycardia
- hypertension_acute
- symptom_count
- respiratory_symptom_count
- gi_symptom_count

## Database Integration

### Patient Management

When a prediction is generated:

1. **Existing Patient**: The chatbot searches for a patient by name
2. **New Patient**: Creates a new patient record if not found
3. **Prediction Storage**: Saves the prediction to `medical_records` table

### Saved Data

```python
{
    'patient_id': int,
    'predicted_disease': str,
    'confidence_score': float,
    'symptoms': str,  # Comma-separated symptom names
    'visit_date': datetime
}
```

## Testing

### Running Tests

```bash
python app/test_chatbot.py
```

### Test Coverage

1. **Symptom Identification**: Tests keyword matching and natural language understanding
2. **Conversation Flow**: Tests complete end-to-end conversation
3. **Patient Info Parsing**: Tests name, age, gender extraction
4. **State Transitions**: Verifies correct state machine behavior
5. **ML Integration**: Tests prediction generation
6. **Data Collection**: Verifies collected data structure

### Expected Output

```
Testing symptom identification...
✅ All symptom identification tests passed!

MEDICAL CHATBOT TEST
============================================================
✅ Conversation started successfully!
✅ Patient info processed successfully!
✅ Symptoms identified successfully!
✅ Symptom questions completed!
✅ Medical history completed!
✅ Prediction generated successfully!
✅ Data collection verified!

ALL TESTS PASSED! ✅
```

## Configuration

### Adjustable Parameters

In `chatbot.py`:

```python
# Maximum symptoms to ask about
if remaining_symptoms and len(self.asked_symptoms) < 8:  # Change 8 to adjust

# Default vital signs (used when not provided)
features['temperature_c'] = 37.5 if features.get('fever', 0) == 1 else 36.5
features['oxygen_saturation'] = 95
features['heart_rate'] = 80
```

## UI Features

### Streamlit Integration

The chatbot page includes:

- **Chat History Display**: Messages with user/bot avatars
- **Chat Input**: Natural text input at bottom
- **New Chat Button**: Reset conversation
- **Help Button**: Display usage instructions
- **Sidebar Stats**: 
  - Message count
  - Symptoms collected
  - Conversation state

### Visual Design

- User messages: 👤 avatar
- Bot messages: 🤖 avatar
- Markdown formatting for rich responses
- Medical disclaimer prominently displayed

## Error Handling

### Graceful Degradation

1. **ML Model Unavailable**: Clear error message, no crash
2. **Database Connection Issues**: Warning displayed, prediction still generated
3. **Invalid Input**: User-friendly prompts for correction
4. **Parsing Errors**: Default values used, conversation continues

### User Feedback

- ✅ Success messages for saved predictions
- ⚠️ Warnings for database issues
- ❌ Clear error messages for failures

## Future Enhancements

### Planned Features

1. **Multi-language Support**: Support for regional languages
2. **Voice Input**: Speech-to-text integration
3. **Advanced NLP**: Better symptom extraction using spaCy/transformers
4. **Personalized Recommendations**: Based on patient history
5. **Appointment Scheduling**: Direct integration with appointment system
6. **PDF Report Generation**: Exportable consultation summary
7. **Triage System**: Urgent vs. non-urgent classification

### Potential Improvements

1. **Context Awareness**: Remember previous conversations
2. **Clarification Questions**: Ask for symptom details (severity, duration)
3. **Differential Diagnosis**: Explain why certain diseases are predicted
4. **Treatment Suggestions**: Basic first-aid recommendations
5. **Follow-up Reminders**: Scheduled check-ins

## Security & Privacy

### Data Protection

- No persistent storage of chat transcripts
- Patient data follows existing database security measures
- Medical records stored with proper access controls
- Disclaimers prominently displayed

### HIPAA Considerations

**Important**: This is a prototype/educational system. For production use:
- Implement encryption for data in transit and at rest
- Add audit logging for all medical data access
- Implement role-based access controls
- Add patient consent workflows
- Ensure compliance with local healthcare regulations

## Support

### Common Issues

**Q: Chatbot doesn't understand my symptoms**
- A: Try using simpler, more direct language (e.g., "I have a fever" instead of "I'm not feeling well")

**Q: Prediction seems inaccurate**
- A: The model has 48% accuracy - always consult a real doctor

**Q: Can't start new conversation**
- A: Click the "🆕 New Chat" button or type 'restart'

**Q: Prediction not saved to database**
- A: Check database connection in main application

## Credits

**Developed by:** Krishna + Omkar  
**Date:** October 13, 2025  
**Phase:** 3 - AI Chatbot Integration  
**Model:** Random Forest (48% accuracy on 8-disease dataset)  
**Framework:** Streamlit + Python 3.11  
**ML Library:** scikit-learn

## License

Part of the Smart Hospital Management System project.
