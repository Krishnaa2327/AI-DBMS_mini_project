import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from app.utils.ml_utils import predict

class UltraChatbot:
    def __init__(self):
        self.state = "greeting"
        self.patient = {}
        self.symptoms = {}
        self.symptom_map = {
            "fever": ["fever", "temperature", "hot"], "cough": ["cough"], "sore_throat": ["sore throat", "throat pain"],
            "fatigue": ["tired", "fatigue", "exhausted"], "headache": ["headache", "head pain"], "nausea": ["nausea"],
            "vomiting": ["vomit", "vomiting"], "diarrhea": ["diarrhea"], "shortness_of_breath": ["short of breath", "breathless"],
            "chest_pain": ["chest pain"], "runny_nose": ["runny nose"], "body_ache": ["body ache"], "loss_of_smell": ["loss of smell"]
        }
    
    def reset(self):
        self.__init__()
    
    def parse_info(self, text):
        try:
            parts = [p.strip() for p in text.split(',')]
            if len(parts) >= 2:
                self.patient = {'name': parts[0].title() if len(parts) >= 3 else 'Patient', 'age': int(parts[-2]), 'gender': parts[-1].capitalize()}
                return True
        except:
            pass
        return False
    
    def find_symptoms(self, text):
        text = text.lower()
        found = []
        for symptom, keywords in self.symptom_map.items():
            if any(kw in text for kw in keywords):
                found.append(symptom)
                self.symptoms[symptom] = 1
        return found
    
    def build_features(self):
        features = {'age': self.patient.get('age', 30), 'sex_encoded': 1 if self.patient.get('gender') == 'Male' else 0}
        for symptom in self.symptom_map.keys():
            features[symptom] = self.symptoms.get(symptom, 0)
        features.update({
            'comorbid_diabetes': 0, 'comorbid_hypertension': 0, 'smoker': 0,
            'temperature_c': 37.5 if features.get('fever', 0) else 36.5, 'oxygen_saturation': 95, 'heart_rate': 80,
            'respiratory_rate': 16, 'bp_systolic': 120, 'bp_diastolic': 80,
            'age_group_encoded': 0 if features['age'] < 18 else 1 if features['age'] < 65 else 2,
            'high_fever': features.get('fever', 0), 'low_oxygen': 0, 'tachycardia': 0, 'hypertension_acute': 0,
            'symptom_count': sum(features.get(s, 0) for s in self.symptom_map.keys()),
            'respiratory_symptom_count': sum([features.get('cough', 0), features.get('sore_throat', 0), features.get('shortness_of_breath', 0)]),
            'gi_symptom_count': sum([features.get('nausea', 0), features.get('vomiting', 0), features.get('diarrhea', 0)])
        })
        return features
    
    def predict_disease(self):
        try:
            features = self.build_features()
            predictions = predict(features, top_k=3)
            if predictions:
                result = f"\n🔮 **Results for {self.patient['name']}**\n\n"
                for i, pred in enumerate(predictions, 1):
                    result += f"{i}. **{pred['disease']}** - {pred['probability']*100:.1f}%\n"
                symptoms_list = [s.replace('_', ' ').title() for s, v in self.symptoms.items() if v == 1]
                if symptoms_list:
                    result += f"\n**Symptoms:** {', '.join(symptoms_list)}\n"
                result += "\n⚠️ **Consult a healthcare provider for proper diagnosis**\nType 'restart' for new consultation."
                self.state = "completed"
                return result
            else:
                return "Sorry, couldn't generate prediction. Try again."
        except Exception as e:
            return f"Prediction error: {str(e)}"
    
    def process_message(self, message):
        message = message.strip()
        msg_lower = message.lower()
        
        if msg_lower in ['quit', 'exit']:
            return "Goodbye! 👋"
        if msg_lower in ['restart', 'reset']:
            self.reset()
            self.state = "info"
            return "Hi! I'm your AI medical assistant. 🤖\n\nProvide: Name, Age, Gender\nExample: 'John, 35, Male'"
        
        if self.state == "greeting":
            self.state = "info"
            return "Hi! I'm your AI medical assistant. 🤖\n\nProvide: Name, Age, Gender\nExample: 'John, 35, Male'"
        elif self.state == "info":
            if self.parse_info(message):
                self.state = "symptoms"
                return f"Thanks {self.patient['name']}!\n\nDescribe your symptoms:\nExample: 'fever, headache, cough'"
            else:
                return "Please use format: 'Name, Age, Gender'"
        elif self.state == "symptoms":
            found = self.find_symptoms(msg_lower)
            if found:
                symptoms_str = ', '.join([s.replace('_', ' ').title() for s in found])
                return f"Found: {symptoms_str}\n\nMore symptoms? Or type 'predict' for diagnosis."
            elif 'predict' in msg_lower:
                if self.symptoms:
                    return self.predict_disease()
                else:
                    return "Please describe symptoms first."
            else:
                return "Describe symptoms like: 'fever and headache' or type 'predict'"
        elif self.state == "completed":
            return "Type 'restart' for new consultation."
        return "Type 'restart' to begin."

_ultra_chatbot = None

def get_ultra_chatbot():
    global _ultra_chatbot
    if _ultra_chatbot is None:
        _ultra_chatbot = UltraChatbot()
    return _ultra_chatbot

def reset_ultra_chatbot():
    global _ultra_chatbot
    _ultra_chatbot = None

if __name__ == "__main__":
    bot = UltraChatbot()
    print(bot.process_message("start"))