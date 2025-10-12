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
    AI Disease Prediction interface (placeholder for now)
    """
    st.markdown("<h1 class='main-header'>🤖 AI Disease Prediction</h1>", unsafe_allow_html=True)
    
    st.info("🚧 **AI Integration Coming Soon!** This page will connect to Omkar's trained ML model.")
    
    # Placeholder UI for prediction interface
    st.subheader("Symptom Input Interface")
    
    with st.form("prediction_form"):
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
        
        with col2:
            st.write("**Symptoms Checklist:**")
            
            # Common symptoms (will be connected to ML model later)
            fever = st.checkbox("Fever")
            cough = st.checkbox("Cough")
            sore_throat = st.checkbox("Sore Throat")
            headache = st.checkbox("Headache")
            nausea = st.checkbox("Nausea")
            vomiting = st.checkbox("Vomiting")
            diarrhea = st.checkbox("Diarrhea")
            fatigue = st.checkbox("Fatigue")
        
        additional_symptoms = st.text_area("Additional Symptoms:", placeholder="Describe any other symptoms...")
        
        predict_button = st.form_submit_button("🔮 Predict Disease", type="primary")
        
        if predict_button:
            # Placeholder prediction logic
            symptoms_list = []
            if fever: symptoms_list.append("fever")
            if cough: symptoms_list.append("cough")
            if sore_throat: symptoms_list.append("sore throat")
            if headache: symptoms_list.append("headache")
            if nausea: symptoms_list.append("nausea")
            if vomiting: symptoms_list.append("vomiting")
            if diarrhea: symptoms_list.append("diarrhea")
            if fatigue: symptoms_list.append("fatigue")
            
            if symptoms_list:
                st.success("🔮 **Prediction Results** (Demo)")
                
                # Mock prediction results
                predicted_disease = "Common Cold" if cough and sore_throat else "Gastroenteritis" if nausea and vomiting else "Migraine"
                confidence = 85.2
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Predicted Disease", predicted_disease)
                with col2:
                    st.metric("Confidence", f"{confidence}%")
                with col3:
                    st.metric("Risk Level", "Medium")
                
                st.write(f"**Symptoms:** {', '.join(symptoms_list)}")
                
                # Save prediction (placeholder)
                st.info("💡 **Note:** This is a demo prediction. Real ML integration coming in next phase!")
            else:
                st.warning("Please select at least one symptom for prediction.")

if __name__ == "__main__":
    main()