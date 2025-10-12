#!/usr/bin/env python3
"""
Smart Hospital Management System - Main Streamlit Application
Created by: Krishna + Omkar
Date: October 12, 2025
Phase: 2 - Streamlit UI Development

Comprehensive hospital management interface with:
- Dashboard with analytics
- Patient management
- Doctor management
- Appointment scheduling
- AI Disease Prediction
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import sys
import os

# Add database module to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from database.connection import db

# Page configuration
st.set_page_config(
    page_title="Smart Hospital Management",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .success-message {
        padding: 1rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        color: #155724;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Dashboard'

def main():
    """
    Main application function
    """
    # Sidebar navigation
    with st.sidebar:
        st.markdown("<h1 style='text-align: center; color: white;'>🏥 Smart Hospital</h1>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # Navigation buttons
        pages = {
            "🏠 Dashboard": "dashboard",
            "👥 Patients": "patients",
            "👩‍⚕️ Doctors": "doctors",
            "📅 Appointments": "appointments",
            "🤖 AI Prediction": "prediction"
        }
        
        for page_name, page_key in pages.items():
            if st.button(page_name, key=page_key, use_container_width=True):
                st.session_state.current_page = page_key
        
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("**Made by:** Krishna + Omkar")
        st.markdown("**Phase:** 2 - UI Development")
    
    # Main content area
    if st.session_state.current_page == 'dashboard':
        dashboard_page()
    elif st.session_state.current_page == 'patients':
        patients_page()
    elif st.session_state.current_page == 'doctors':
        doctors_page()
    elif st.session_state.current_page == 'appointments':
        appointments_page()
    elif st.session_state.current_page == 'prediction':
        prediction_page()

# =====================================================
# DASHBOARD PAGE
# =====================================================

def dashboard_page():
    """
    Hospital dashboard with analytics and overview
    """
    st.markdown("<h1 class='main-header'>🏥 Hospital Dashboard</h1>", unsafe_allow_html=True)
    
    try:
        # Get dashboard statistics
        stats = db.get_dashboard_stats()
        
        # Key metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="👥 Total Patients",
                value=stats['total_patients'],
                delta=f"+{stats['total_patients'] - 5} this month"
            )
        
        with col2:
            st.metric(
                label="👩‍⚕️ Total Doctors",
                value=stats['total_doctors'],
                delta=None
            )
        
        with col3:
            st.metric(
                label="📅 Scheduled",
                value=stats['scheduled_appointments'],
                delta=f"+{stats['scheduled_appointments']} upcoming"
            )
        
        with col4:
            st.metric(
                label="📊 Today's Visits",
                value=stats['todays_visits'],
                delta=f"{stats['todays_visits']} today"
            )
        
        st.markdown("---")
        
        # Charts row
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Upcoming Appointments")
            if stats['upcoming_appointments']:
                upcoming_df = pd.DataFrame(stats['upcoming_appointments'])
                upcoming_df['appointment_date'] = pd.to_datetime(upcoming_df['appointment_date'])
                upcoming_df['date'] = upcoming_df['appointment_date'].dt.strftime('%Y-%m-%d')
                
                st.dataframe(
                    upcoming_df[['patient_name', 'doctor_name', 'date']],
                    use_container_width=True
                )
            else:
                st.info("No upcoming appointments scheduled")
        
        with col2:
            st.subheader("🔍 Top Predicted Diseases")
            if stats['top_predicted_diseases']:
                diseases_df = pd.DataFrame(stats['top_predicted_diseases'])
                
                fig = px.pie(
                    diseases_df,
                    values='count',
                    names='predicted_disease',
                    title="Disease Predictions Distribution"
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No disease predictions yet")
        
        # Recent activity
        st.subheader("📋 Recent Activity")
        
        # Get recent patients
        recent_patients = db.get_patients(limit=5)
        if recent_patients:
            patients_df = pd.DataFrame(recent_patients)
            patients_df['created_at'] = pd.to_datetime(patients_df['created_at'])
            
            st.write("**Recently Registered Patients:**")
            st.dataframe(
                patients_df[['name', 'age', 'gender', 'contact', 'created_at']],
                use_container_width=True
            )
        
    except Exception as e:
        st.error(f"Error loading dashboard: {e}")
        st.info("Please check your database connection.")

# =====================================================
# PATIENTS PAGE
# =====================================================

def patients_page():
    """
    Patient management interface
    """
    st.markdown("<h1 class='main-header'>👥 Patient Management</h1>", unsafe_allow_html=True)
    
    # Tabs for different patient operations
    tab1, tab2, tab3 = st.tabs(["📋 View Patients", "➕ Add Patient", "✏️ Update Patient"])
    
    with tab1:
        st.subheader("All Patients")
        
        try:
            patients = db.get_patients()
            if patients:
                df = pd.DataFrame(patients)
                df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d %H:%M')
                
                # Search functionality
                search_term = st.text_input("🔍 Search patients by name:", "")
                if search_term:
                    df = df[df['name'].str.contains(search_term, case=False, na=False)]
                
                # Display patients table
                st.dataframe(
                    df[['patient_id', 'name', 'age', 'gender', 'contact', 'address', 'created_at']],
                    use_container_width=True
                )
                
                st.success(f"Total patients: {len(df)}")
                
            else:
                st.info("No patients found. Add some patients to get started!")
                
        except Exception as e:
            st.error(f"Error fetching patients: {e}")
    
    with tab2:
        st.subheader("Add New Patient")
        
        with st.form("add_patient_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Patient Name *", placeholder="Enter full name")
                age = st.number_input("Age *", min_value=1, max_value=150, value=30)
                gender = st.selectbox("Gender *", ["Male", "Female", "Other"])
            
            with col2:
                contact = st.text_input("Contact Number", placeholder="10-digit phone number")
                address = st.text_area("Address", placeholder="Complete address")
            
            submitted = st.form_submit_button("Add Patient", type="primary")
            
            if submitted:
                if name:
                    try:
                        patient_id = db.add_patient(name, age, gender, contact, address)
                        st.success(f"✅ Patient '{name}' added successfully! Patient ID: {patient_id}")
                        st.balloons()
                    except Exception as e:
                        st.error(f"Error adding patient: {e}")
                else:
                    st.error("Please enter patient name!")
    
    with tab3:
        st.subheader("Update Patient Information")
        
        try:
            patients = db.get_patients()
            if patients:
                # Select patient to update
                patient_options = {f"{p['name']} (ID: {p['patient_id']})": p['patient_id'] for p in patients}
                selected_patient = st.selectbox("Select Patient to Update:", list(patient_options.keys()))
                
                if selected_patient:
                    patient_id = patient_options[selected_patient]
                    patient_data = db.get_patient_by_id(patient_id)
                    
                    if patient_data:
                        with st.form("update_patient_form"):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                new_name = st.text_input("Name", value=patient_data['name'])
                                new_age = st.number_input("Age", min_value=1, max_value=150, value=patient_data['age'])
                                new_gender = st.selectbox("Gender", ["Male", "Female", "Other"], 
                                                        index=["Male", "Female", "Other"].index(patient_data['gender']))
                            
                            with col2:
                                new_contact = st.text_input("Contact", value=patient_data['contact'] or "")
                                new_address = st.text_area("Address", value=patient_data['address'] or "")
                            
                            updated = st.form_submit_button("Update Patient", type="primary")
                            
                            if updated:
                                try:
                                    updates = {
                                        'name': new_name,
                                        'age': new_age,
                                        'gender': new_gender,
                                        'contact': new_contact if new_contact else None,
                                        'address': new_address if new_address else None
                                    }
                                    
                                    success = db.update_patient(patient_id, **updates)
                                    if success:
                                        st.success("✅ Patient updated successfully!")
                                    else:
                                        st.error("Failed to update patient")
                                        
                                except Exception as e:
                                    st.error(f"Error updating patient: {e}")
            else:
                st.info("No patients available to update")
                
        except Exception as e:
            st.error(f"Error loading patients: {e}")

# =====================================================
# DOCTORS PAGE
# =====================================================

def doctors_page():
    """
    Doctor management interface
    """
    st.markdown("<h1 class='main-header'>👩‍⚕️ Doctor Management</h1>", unsafe_allow_html=True)
    
    # Tabs for doctor operations
    tab1, tab2 = st.tabs(["📋 View Doctors", "➕ Add Doctor"])
    
    with tab1:
        st.subheader("All Doctors")
        
        try:
            doctors = db.get_doctors()
            if doctors:
                df = pd.DataFrame(doctors)
                df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d %H:%M')
                
                # Filter by specialization
                specializations = ['All'] + list(df['specialization'].unique())
                selected_spec = st.selectbox("Filter by Specialization:", specializations)
                
                if selected_spec != 'All':
                    df = df[df['specialization'] == selected_spec]
                
                st.dataframe(
                    df[['doctor_id', 'name', 'specialization', 'contact', 'email', 'created_at']],
                    use_container_width=True
                )
                
                st.success(f"Total doctors: {len(df)}")
                
            else:
                st.info("No doctors found. Add some doctors to get started!")
                
        except Exception as e:
            st.error(f"Error fetching doctors: {e}")
    
    with tab2:
        st.subheader("Add New Doctor")
        
        with st.form("add_doctor_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Doctor Name *", placeholder="Dr. John Doe")
                specialization = st.selectbox("Specialization *", [
                    "Cardiology", "Pediatrics", "Neurology", "Dermatology", 
                    "Orthopedics", "Gynecology", "Psychiatry", "General Medicine",
                    "Surgery", "Radiology", "Pathology", "Other"
                ])
            
            with col2:
                contact = st.text_input("Contact Number", placeholder="10-digit phone number")
                email = st.text_input("Email", placeholder="doctor@hospital.com")
            
            submitted = st.form_submit_button("Add Doctor", type="primary")
            
            if submitted:
                if name and specialization:
                    try:
                        doctor_id = db.add_doctor(name, specialization, contact, email)
                        st.success(f"✅ Doctor '{name}' added successfully! Doctor ID: {doctor_id}")
                        st.balloons()
                    except Exception as e:
                        st.error(f"Error adding doctor: {e}")
                else:
                    st.error("Please enter doctor name and specialization!")

# =====================================================
# APPOINTMENTS PAGE
# =====================================================

def appointments_page():
    """
    Appointment management interface
    """
    st.markdown("<h1 class='main-header'>📅 Appointment Management</h1>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📋 View Appointments", "➕ Schedule Appointment", "✏️ Update Status"])
    
    with tab1:
        st.subheader("All Appointments")
        
        try:
            # Filters
            col1, col2, col3 = st.columns(3)
            
            with col1:
                status_filter = st.selectbox("Filter by Status:", ['All', 'Scheduled', 'Completed', 'Cancelled'])
            
            with col2:
                date_from = st.date_input("From Date:", value=date.today() - timedelta(days=30))
            
            with col3:
                date_to = st.date_input("To Date:", value=date.today() + timedelta(days=30))
            
            # Get appointments based on filters
            appointments = db.get_appointments(
                status=None if status_filter == 'All' else status_filter,
                date_from=date_from,
                date_to=date_to
            )
            
            if appointments:
                df = pd.DataFrame(appointments)
                df['appointment_date'] = pd.to_datetime(df['appointment_date']).dt.strftime('%Y-%m-%d %H:%M')
                
                st.dataframe(
                    df[['appointment_id', 'patient_name', 'doctor_name', 'specialization', 
                       'appointment_date', 'status', 'notes']],
                    use_container_width=True
                )
                
                st.success(f"Total appointments: {len(df)}")
            else:
                st.info("No appointments found for the selected criteria")
                
        except Exception as e:
            st.error(f"Error fetching appointments: {e}")
    
    with tab2:
        st.subheader("Schedule New Appointment")
        
        try:
            patients = db.get_patients()
            doctors = db.get_doctors()
            
            if patients and doctors:
                with st.form("schedule_appointment_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Patient selection
                        patient_options = {f"{p['name']} (ID: {p['patient_id']})": p['patient_id'] for p in patients}
                        selected_patient = st.selectbox("Select Patient *", list(patient_options.keys()))
                        
                        # Doctor selection
                        doctor_options = {f"Dr. {d['name']} - {d['specialization']}": d['doctor_id'] for d in doctors}
                        selected_doctor = st.selectbox("Select Doctor *", list(doctor_options.keys()))
                    
                    with col2:
                        appointment_date = st.date_input("Appointment Date *", min_value=date.today())
                        appointment_time = st.time_input("Appointment Time *", value=datetime.now().time())
                        notes = st.text_area("Notes", placeholder="Any special instructions or notes")
                    
                    submitted = st.form_submit_button("Schedule Appointment", type="primary")
                    
                    if submitted:
                        if selected_patient and selected_doctor:
                            try:
                                patient_id = patient_options[selected_patient]
                                doctor_id = doctor_options[selected_doctor]
                                
                                appointment_datetime = datetime.combine(appointment_date, appointment_time)
                                
                                appointment_id = db.schedule_appointment(
                                    patient_id, doctor_id, appointment_datetime, notes
                                )
                                
                                st.success(f"✅ Appointment scheduled successfully! Appointment ID: {appointment_id}")
                                st.balloons()
                                
                            except Exception as e:
                                st.error(f"Error scheduling appointment: {e}")
                        else:
                            st.error("Please select both patient and doctor!")
            else:
                st.warning("Please add patients and doctors first before scheduling appointments.")
                
        except Exception as e:
            st.error(f"Error loading data: {e}")
    
    with tab3:
        st.subheader("Update Appointment Status")
        
        try:
            appointments = db.get_appointments(status='Scheduled')
            
            if appointments:
                appointment_options = {f"#{a['appointment_id']} - {a['patient_name']} with Dr. {a['doctor_name']} ({a['appointment_date']})": a['appointment_id'] for a in appointments}
                selected_appointment = st.selectbox("Select Appointment:", list(appointment_options.keys()))
                
                if selected_appointment:
                    new_status = st.selectbox("New Status:", ['Completed', 'Cancelled'])
                    
                    if st.button("Update Status", type="primary"):
                        try:
                            appointment_id = appointment_options[selected_appointment]
                            success = db.update_appointment_status(appointment_id, new_status)
                            
                            if success:
                                st.success(f"✅ Appointment status updated to {new_status}!")
                            else:
                                st.error("Failed to update appointment status")
                                
                        except Exception as e:
                            st.error(f"Error updating appointment: {e}")
            else:
                st.info("No scheduled appointments to update")
                
        except Exception as e:
            st.error(f"Error loading appointments: {e}")

# =====================================================
# AI PREDICTION PAGE
# =====================================================

def prediction_page():
    """
    AI Disease Prediction interface with real ML integration
    """
    st.markdown("<h1 class='main-header'>🤖 AI Disease Prediction</h1>", unsafe_allow_html=True)
    
    st.success("🔬 **AI Model Active!** Using trained Random Forest model with 48% accuracy.")
    
    # Import ML utilities
    try:
        from utils.ml_utils import predict, load_resources
        ml_available = True
        st.info("✅ ML model loaded successfully!")
    except Exception as e:
        st.error(f"❌ ML model loading failed: {e}")
        ml_available = False
    
    # Tabs for different prediction interfaces
    tab1, tab2, tab3 = st.tabs(["🔮 Quick Prediction", "📊 Advanced Prediction", "📈 Prediction History"])
    
    with tab1:
        st.subheader("Quick Disease Prediction")
        
        with st.form("quick_prediction_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Patient Information:**")
                patients = []
                try:
                    patients = db.get_patients(limit=50)
                except:
                    pass
                    
                if patients:
                    patient_options = {f"{p['name']} (ID: {p['patient_id']})": p['patient_id'] for p in patients}
                    selected_patient = st.selectbox("Select Patient:", ['New Patient'] + list(patient_options.keys()))
                else:
                    selected_patient = 'New Patient'
                
                if selected_patient == 'New Patient':
                    patient_name = st.text_input("Patient Name:")
                    patient_age = st.number_input("Age:", min_value=1, max_value=150, value=30)
                    patient_gender = st.selectbox("Gender:", ["Male", "Female", "Other"])
                else:
                    patient_id = patient_options[selected_patient]
                    patient_data = db.get_patient_by_id(patient_id)
                    if patient_data:
                        patient_name = patient_data['name']
                        patient_age = patient_data['age']
                        patient_gender = patient_data['gender']
                        st.write(f"**Selected:** {patient_name} (Age: {patient_age}, Gender: {patient_gender})")
            
            with col2:
                st.write("**Core Symptoms:**")
                
                # Core symptoms for quick prediction
                fever = st.checkbox("Fever")
                cough = st.checkbox("Cough")
                sore_throat = st.checkbox("Sore Throat")
                headache = st.checkbox("Headache")
                nausea = st.checkbox("Nausea")
                vomiting = st.checkbox("Vomiting")
                diarrhea = st.checkbox("Diarrhea")
                fatigue = st.checkbox("Fatigue")
                shortness_of_breath = st.checkbox("Shortness of Breath")
                body_ache = st.checkbox("Body Ache")
            
            predict_button = st.form_submit_button("🔮 Predict Disease", type="primary")
            
            if predict_button:
                if ml_available:
                    try:
                        # Prepare features for ML model
                        features = {
                            'age': patient_age,
                            'sex_encoded': 1 if patient_gender == 'Male' else 0,
                            'fever': 1 if fever else 0,
                            'cough': 1 if cough else 0,
                            'sore_throat': 1 if sore_throat else 0,
                            'headache': 1 if headache else 0,
                            'nausea': 1 if nausea else 0,
                            'vomiting': 1 if vomiting else 0,
                            'diarrhea': 1 if diarrhea else 0,
                            'fatigue': 1 if fatigue else 0,
                            'shortness_of_breath': 1 if shortness_of_breath else 0,
                            'body_ache': 1 if body_ache else 0,
                            # Default values for missing features
                            'temperature_c': 37.5 if fever else 36.5,
                            'oxygen_saturation': 95,
                            'heart_rate': 80,
                            'respiratory_rate': 16,
                            'bp_systolic': 120,
                            'bp_diastolic': 80,
                            'comorbid_diabetes': 0,
                            'comorbid_hypertension': 0,
                            'smoker': 0,
                            'chest_pain': 0,
                            'runny_nose': 0,
                            'loss_of_smell': 0,
                            'age_group_encoded': 0 if patient_age < 18 else 1 if patient_age < 65 else 2,
                            'high_fever': 1 if fever else 0,
                            'low_oxygen': 0,
                            'tachycardia': 0,
                            'hypertension_acute': 0,
                            'symptom_count': sum([fever, cough, sore_throat, headache, nausea, vomiting, diarrhea, fatigue, shortness_of_breath, body_ache]),
                            'respiratory_symptom_count': sum([cough, sore_throat, shortness_of_breath]),
                            'gi_symptom_count': sum([nausea, vomiting, diarrhea])
                        }
                        
                        # Get predictions
                        predictions = predict(features, top_k=3)
                        
                        if predictions:
                            st.success("🔮 **AI Prediction Results**")
                            
                            # Display top prediction
                            top_prediction = predictions[0]
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Predicted Disease", top_prediction['disease'])
                            with col2:
                                st.metric("Confidence", f"{top_prediction['probability']*100:.1f}%")
                            with col3:
                                risk_level = "High" if top_prediction['probability'] > 0.7 else "Medium" if top_prediction['probability'] > 0.4 else "Low"
                                st.metric("Risk Level", risk_level)
                            
                            # Show all predictions
                            st.subheader("Top 3 Predictions:")
                            for i, pred in enumerate(predictions, 1):
                                st.write(f"{i}. **{pred['disease']}** - {pred['probability']*100:.1f}% confidence")
                            
                            # Collect symptoms for saving
                            symptoms_list = []
                            if fever: symptoms_list.append("fever")
                            if cough: symptoms_list.append("cough")
                            if sore_throat: symptoms_list.append("sore throat")
                            if headache: symptoms_list.append("headache")
                            if nausea: symptoms_list.append("nausea")
                            if vomiting: symptoms_list.append("vomiting")
                            if diarrhea: symptoms_list.append("diarrhea")
                            if fatigue: symptoms_list.append("fatigue")
                            if shortness_of_breath: symptoms_list.append("shortness of breath")
                            if body_ache: symptoms_list.append("body ache")
                            
                            symptoms_text = ", ".join(symptoms_list)
                            st.write(f"**Symptoms:** {symptoms_text}")
                            
                            # Save prediction to database
                            try:
                                if selected_patient != 'New Patient':
                                    # Existing patient
                                    record_id = db.save_prediction(
                                        patient_id=patient_options[selected_patient],
                                        predicted_disease=top_prediction['disease'],
                                        confidence_score=top_prediction['probability'],
                                        symptoms=symptoms_text
                                    )
                                    st.success(f"✅ Prediction saved to patient record! Record ID: {record_id}")
                                else:
                                    # New patient - add to database first
                                    if patient_name:
                                        new_patient_id = db.add_patient(patient_name, patient_age, patient_gender)
                                        record_id = db.save_prediction(
                                            patient_id=new_patient_id,
                                            predicted_disease=top_prediction['disease'],
                                            confidence_score=top_prediction['probability'],
                                            symptoms=symptoms_text
                                        )
                                        st.success(f"✅ New patient added and prediction saved! Patient ID: {new_patient_id}, Record ID: {record_id}")
                                    else:
                                        st.warning("Please enter patient name to save prediction")
                                        
                            except Exception as e:
                                st.error(f"❌ Error saving prediction: {e}")
                                
                    except Exception as e:
                        st.error(f"❌ Prediction failed: {e}")
                        st.write("**Debug info:**", str(e))
                else:
                    st.error("❌ ML model not available. Please check the model files.")
    
    with tab2:
        st.subheader("Advanced Disease Prediction")
        st.info("📊 Comprehensive prediction using all 32 medical features")
        
        with st.form("advanced_prediction_form"):
            # Patient Information Section
            st.write("### 👤 Patient Information")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                patients = []
                try:
                    patients = db.get_patients(limit=50)
                except:
                    pass
                    
                if patients:
                    patient_options = {f"{p['name']} (ID: {p['patient_id']})": p['patient_id'] for p in patients}
                    selected_patient_adv = st.selectbox("Select Patient:", ['New Patient'] + list(patient_options.keys()), key="adv_patient")
                else:
                    selected_patient_adv = 'New Patient'
                
                if selected_patient_adv == 'New Patient':
                    patient_name_adv = st.text_input("Patient Name:", key="adv_name")
                    patient_age_adv = st.number_input("Age:", min_value=1, max_value=150, value=30, key="adv_age")
                    patient_gender_adv = st.selectbox("Gender:", ["Male", "Female", "Other"], key="adv_gender")
                else:
                    patient_id = patient_options[selected_patient_adv]
                    patient_data = db.get_patient_by_id(patient_id)
                    if patient_data:
                        patient_name_adv = patient_data['name']
                        patient_age_adv = patient_data['age']
                        patient_gender_adv = patient_data['gender']
                        st.write(f"**Selected:** {patient_name_adv} (Age: {patient_age_adv}, Gender: {patient_gender_adv})")
            
            with col2:
                st.write("**Medical History:**")
                comorbid_diabetes = st.checkbox("Diabetes", key="diabetes")
                comorbid_hypertension = st.checkbox("Hypertension", key="hypertension")
                smoker = st.checkbox("Smoker", key="smoker")
            
            with col3:
                st.write("**Vital Signs:**")
                temperature = st.number_input("Temperature (°C):", min_value=35.0, max_value=42.0, value=36.5, step=0.1, key="temp")
                oxygen_sat = st.number_input("Oxygen Saturation (%):", min_value=70, max_value=100, value=98, key="o2")
                heart_rate = st.number_input("Heart Rate (bpm):", min_value=40, max_value=200, value=72, key="hr")
            
            # More vital signs
            col4, col5, col6 = st.columns(3)
            with col4:
                respiratory_rate = st.number_input("Respiratory Rate (/min):", min_value=8, max_value=40, value=16, key="rr")
            with col5:
                bp_systolic = st.number_input("BP Systolic (mmHg):", min_value=80, max_value=250, value=120, key="sys")
            with col6:
                bp_diastolic = st.number_input("BP Diastolic (mmHg):", min_value=40, max_value=150, value=80, key="dia")
            
            # Symptoms Section
            st.write("### 🩺 Symptoms Checklist")
            
            # Primary symptoms
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.write("**General:**")
                fever_adv = st.checkbox("Fever", key="fever_adv")
                fatigue_adv = st.checkbox("Fatigue", key="fatigue_adv")
                headache_adv = st.checkbox("Headache", key="headache_adv")
                body_ache_adv = st.checkbox("Body Ache", key="body_ache_adv")
            
            with col2:
                st.write("**Respiratory:**")
                cough_adv = st.checkbox("Cough", key="cough_adv")
                sore_throat_adv = st.checkbox("Sore Throat", key="sore_throat_adv")
                shortness_of_breath_adv = st.checkbox("Shortness of Breath", key="sob_adv")
                chest_pain_adv = st.checkbox("Chest Pain", key="chest_pain_adv")
                runny_nose_adv = st.checkbox("Runny Nose", key="runny_nose_adv")
            
            with col3:
                st.write("**Gastrointestinal:**")
                nausea_adv = st.checkbox("Nausea", key="nausea_adv")
                vomiting_adv = st.checkbox("Vomiting", key="vomiting_adv")
                diarrhea_adv = st.checkbox("Diarrhea", key="diarrhea_adv")
            
            with col4:
                st.write("**Other:**")
                loss_of_smell_adv = st.checkbox("Loss of Smell", key="smell_adv")
            
            predict_button_adv = st.form_submit_button("🔬 Advanced Prediction", type="primary")
            
            if predict_button_adv:
                if ml_available:
                    try:
                        # Prepare comprehensive features for ML model
                        features_adv = {
                            'age': patient_age_adv,
                            'sex_encoded': 1 if patient_gender_adv == 'Male' else 0,
                            'comorbid_diabetes': 1 if comorbid_diabetes else 0,
                            'comorbid_hypertension': 1 if comorbid_hypertension else 0,
                            'smoker': 1 if smoker else 0,
                            'temperature_c': temperature,
                            'oxygen_saturation': oxygen_sat,
                            'heart_rate': heart_rate,
                            'respiratory_rate': respiratory_rate,
                            'bp_systolic': bp_systolic,
                            'bp_diastolic': bp_diastolic,
                            'fever': 1 if fever_adv else 0,
                            'cough': 1 if cough_adv else 0,
                            'sore_throat': 1 if sore_throat_adv else 0,
                            'fatigue': 1 if fatigue_adv else 0,
                            'headache': 1 if headache_adv else 0,
                            'nausea': 1 if nausea_adv else 0,
                            'vomiting': 1 if vomiting_adv else 0,
                            'diarrhea': 1 if diarrhea_adv else 0,
                            'shortness_of_breath': 1 if shortness_of_breath_adv else 0,
                            'chest_pain': 1 if chest_pain_adv else 0,
                            'runny_nose': 1 if runny_nose_adv else 0,
                            'body_ache': 1 if body_ache_adv else 0,
                            'loss_of_smell': 1 if loss_of_smell_adv else 0,
                            # Engineered features
                            'age_group_encoded': 0 if patient_age_adv < 18 else 1 if patient_age_adv < 65 else 2,
                            'high_fever': 1 if temperature > 38.5 else 0,
                            'low_oxygen': 1 if oxygen_sat < 95 else 0,
                            'tachycardia': 1 if heart_rate > 100 else 0,
                            'hypertension_acute': 1 if bp_systolic > 140 or bp_diastolic > 90 else 0,
                            'symptom_count': sum([fever_adv, cough_adv, sore_throat_adv, fatigue_adv, headache_adv, nausea_adv, vomiting_adv, diarrhea_adv, shortness_of_breath_adv, chest_pain_adv, runny_nose_adv, body_ache_adv, loss_of_smell_adv]),
                            'respiratory_symptom_count': sum([cough_adv, sore_throat_adv, shortness_of_breath_adv]),
                            'gi_symptom_count': sum([nausea_adv, vomiting_adv, diarrhea_adv])
                        }
                        
                        # Get predictions
                        predictions_adv = predict(features_adv, top_k=5)
                        
                        if predictions_adv:
                            st.success("🔬 **Advanced AI Prediction Results**")
                            
                            # Display comprehensive results
                            top_prediction_adv = predictions_adv[0]
                            
                            # Metrics row
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric("Primary Disease", top_prediction_adv['disease'])
                            with col2:
                                st.metric("Confidence", f"{top_prediction_adv['probability']*100:.1f}%")
                            with col3:
                                risk_level = "High" if top_prediction_adv['probability'] > 0.7 else "Medium" if top_prediction_adv['probability'] > 0.4 else "Low"
                                st.metric("Risk Level", risk_level)
                            with col4:
                                total_symptoms = features_adv['symptom_count']
                                st.metric("Total Symptoms", total_symptoms)
                            
                            # Detailed predictions table
                            st.subheader("📊 Top 5 Differential Diagnoses:")
                            pred_data = []
                            for i, pred in enumerate(predictions_adv, 1):
                                pred_data.append({
                                    "Rank": i,
                                    "Disease": pred['disease'],
                                    "Probability": f"{pred['probability']*100:.1f}%",
                                    "Confidence": "High" if pred['probability'] > 0.6 else "Medium" if pred['probability'] > 0.3 else "Low"
                                })
                            
                            pred_df = pd.DataFrame(pred_data)
                            st.dataframe(pred_df, use_container_width=True)
                            
                            # Feature importance display
                            st.subheader("🔍 Clinical Summary:")
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.write("**Vital Signs Assessment:**")
                                if features_adv['high_fever']:
                                    st.warning("⚠️ High fever detected")
                                if features_adv['low_oxygen']:
                                    st.error("🚨 Low oxygen saturation")
                                if features_adv['tachycardia']:
                                    st.warning("⚠️ Elevated heart rate")
                                if features_adv['hypertension_acute']:
                                    st.warning("⚠️ Elevated blood pressure")
                                
                                st.write(f"- Temperature: {temperature}°C")
                                st.write(f"- O2 Saturation: {oxygen_sat}%")
                                st.write(f"- Heart Rate: {heart_rate} bpm")
                                st.write(f"- BP: {bp_systolic}/{bp_diastolic} mmHg")
                            
                            with col2:
                                st.write("**Symptom Analysis:**")
                                st.write(f"- Total symptoms: {total_symptoms}")
                                st.write(f"- Respiratory symptoms: {features_adv['respiratory_symptom_count']}")
                                st.write(f"- GI symptoms: {features_adv['gi_symptom_count']}")
                                
                                if comorbid_diabetes or comorbid_hypertension or smoker:
                                    st.write("**Risk Factors:**")
                                    if comorbid_diabetes:
                                        st.write("- Diabetes mellitus")
                                    if comorbid_hypertension:
                                        st.write("- Hypertension")
                                    if smoker:
                                        st.write("- Smoking history")
                            
                            # Save prediction to database
                            try:
                                # Collect all symptoms for saving
                                symptoms_list_adv = []
                                if fever_adv: symptoms_list_adv.append("fever")
                                if cough_adv: symptoms_list_adv.append("cough")
                                if sore_throat_adv: symptoms_list_adv.append("sore throat")
                                if fatigue_adv: symptoms_list_adv.append("fatigue")
                                if headache_adv: symptoms_list_adv.append("headache")
                                if nausea_adv: symptoms_list_adv.append("nausea")
                                if vomiting_adv: symptoms_list_adv.append("vomiting")
                                if diarrhea_adv: symptoms_list_adv.append("diarrhea")
                                if shortness_of_breath_adv: symptoms_list_adv.append("shortness of breath")
                                if chest_pain_adv: symptoms_list_adv.append("chest pain")
                                if runny_nose_adv: symptoms_list_adv.append("runny nose")
                                if body_ache_adv: symptoms_list_adv.append("body ache")
                                if loss_of_smell_adv: symptoms_list_adv.append("loss of smell")
                                
                                symptoms_text_adv = ", ".join(symptoms_list_adv)
                                
                                if selected_patient_adv != 'New Patient':
                                    # Existing patient
                                    record_id = db.save_prediction(
                                        patient_id=patient_options[selected_patient_adv],
                                        predicted_disease=top_prediction_adv['disease'],
                                        confidence_score=top_prediction_adv['probability'],
                                        symptoms=symptoms_text_adv
                                    )
                                    st.success(f"✅ Advanced prediction saved to patient record! Record ID: {record_id}")
                                else:
                                    # New patient - add to database first
                                    if patient_name_adv:
                                        new_patient_id = db.add_patient(patient_name_adv, patient_age_adv, patient_gender_adv)
                                        record_id = db.save_prediction(
                                            patient_id=new_patient_id,
                                            predicted_disease=top_prediction_adv['disease'],
                                            confidence_score=top_prediction_adv['probability'],
                                            symptoms=symptoms_text_adv
                                        )
                                        st.success(f"✅ New patient added and advanced prediction saved! Patient ID: {new_patient_id}, Record ID: {record_id}")
                                    else:
                                        st.warning("Please enter patient name to save prediction")
                                        
                            except Exception as e:
                                st.error(f"❌ Error saving advanced prediction: {e}")
                                
                    except Exception as e:
                        st.error(f"❌ Advanced prediction failed: {e}")
                        st.write("**Debug info:**", str(e))
                else:
                    st.error("❌ ML model not available. Please check the model files.")
    
    with tab3:
        st.subheader("📈 AI Prediction History")
        
        # Filters for history
        col1, col2, col3 = st.columns(3)
        with col1:
            # Patient filter
            try:
                patients = db.get_patients(limit=100)
                if patients:
                    patient_options = {'All Patients': None}
                    patient_options.update({f"{p['name']} (ID: {p['patient_id']})": p['patient_id'] for p in patients})
                    selected_patient_filter = st.selectbox("Filter by Patient:", list(patient_options.keys()))
                    patient_filter = patient_options[selected_patient_filter]
                else:
                    patient_filter = None
            except:
                patient_filter = None
        
        with col2:
            # Disease filter
            disease_filter = st.selectbox("Filter by Disease:", [
                'All Diseases', 'COVID-19', 'Common Cold', 'Pneumonia', 
                'Allergic Rhinitis', 'Food Poisoning', 'Gastroenteritis', 
                'Migraine', 'Urinary Tract Infection'
            ])
        
        with col3:
            # Date range
            date_range = st.date_input("From Date:", value=date.today() - timedelta(days=30))
        
        # Get prediction history
        try:
            conn = db.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Build query with filters
            query = """
            SELECT mr.record_id, mr.patient_id, p.name as patient_name, 
                   mr.predicted_disease, mr.confidence_score, mr.symptoms,
                   mr.visit_date, p.age, p.gender
            FROM medical_records mr
            JOIN patients p ON mr.patient_id = p.patient_id
            WHERE mr.predicted_disease IS NOT NULL
            """
            
            params = []
            
            if patient_filter:
                query += " AND mr.patient_id = %s"
                params.append(patient_filter)
            
            if disease_filter != 'All Diseases':
                query += " AND mr.predicted_disease = %s"
                params.append(disease_filter)
            
            query += " AND DATE(mr.visit_date) >= %s"
            params.append(date_range)
            
            query += " ORDER BY mr.visit_date DESC LIMIT 100"
            
            cursor.execute(query, params)
            predictions_history = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            if predictions_history:
                # Convert to DataFrame
                df_history = pd.DataFrame(predictions_history)
                df_history['visit_date'] = pd.to_datetime(df_history['visit_date']).dt.strftime('%Y-%m-%d %H:%M')
                df_history['confidence_percentage'] = (df_history['confidence_score'] * 100).round(1)
                
                # Summary statistics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Predictions", len(df_history))
                with col2:
                    avg_confidence = df_history['confidence_score'].mean() * 100
                    st.metric("Avg Confidence", f"{avg_confidence:.1f}%")
                with col3:
                    most_common_disease = df_history['predicted_disease'].mode().iloc[0] if not df_history.empty else "N/A"
                    st.metric("Most Predicted", most_common_disease)
                with col4:
                    unique_patients = df_history['patient_id'].nunique()
                    st.metric("Unique Patients", unique_patients)
                
                # Visualizations
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📈 Disease Distribution")
                    disease_counts = df_history['predicted_disease'].value_counts()
                    if len(disease_counts) > 0:
                        fig_pie = px.pie(
                            values=disease_counts.values,
                            names=disease_counts.index,
                            title="Predicted Diseases Distribution"
                        )
                        st.plotly_chart(fig_pie, use_container_width=True)
                
                with col2:
                    st.subheader("📈 Confidence Distribution")
                    fig_hist = px.histogram(
                        df_history,
                        x='confidence_percentage',
                        nbins=10,
                        title="Confidence Score Distribution",
                        labels={'confidence_percentage': 'Confidence (%)', 'count': 'Number of Predictions'}
                    )
                    st.plotly_chart(fig_hist, use_container_width=True)
                
                # Prediction timeline
                st.subheader("🕰️ Prediction Timeline")
                df_timeline = df_history.copy()
                df_timeline['date'] = pd.to_datetime(df_timeline['visit_date'], format='%Y-%m-%d %H:%M')
                daily_counts = df_timeline.groupby(df_timeline['date'].dt.date).size().reset_index()
                daily_counts.columns = ['date', 'predictions']
                
                if len(daily_counts) > 0:
                    fig_timeline = px.line(
                        daily_counts,
                        x='date',
                        y='predictions',
                        title="Daily Predictions Over Time",
                        markers=True
                    )
                    st.plotly_chart(fig_timeline, use_container_width=True)
                
                # Detailed history table
                st.subheader("📋 Detailed Prediction History")
                
                # Search functionality
                search_term = st.text_input("🔍 Search in symptoms or disease:", "")
                if search_term:
                    mask = df_history['predicted_disease'].str.contains(search_term, case=False, na=False) | \
                           df_history['symptoms'].str.contains(search_term, case=False, na=False)
                    df_history = df_history[mask]
                
                # Display table
                display_columns = ['record_id', 'patient_name', 'predicted_disease', 'confidence_percentage', 'symptoms', 'visit_date']
                st.dataframe(
                    df_history[display_columns].rename(columns={
                        'record_id': 'Record ID',
                        'patient_name': 'Patient',
                        'predicted_disease': 'Predicted Disease',
                        'confidence_percentage': 'Confidence %',
                        'symptoms': 'Symptoms',
                        'visit_date': 'Date'
                    }),
                    use_container_width=True
                )
                
                # Export option
                if st.button("📎 Export History to CSV"):
                    csv = df_history.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name=f"prediction_history_{date.today()}.csv",
                        mime="text/csv"
                    )
                
            else:
                st.info("📈 No prediction history found for the selected filters.")
                st.write("Try adjusting your filters or make some predictions first!")
                
        except Exception as e:
            st.error(f"❌ Error loading prediction history: {e}")
            st.write("**Debug info:**", str(e))

if __name__ == "__main__":
    main()
