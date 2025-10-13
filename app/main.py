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
    /* Main Header Styling */
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 2rem;
        padding: 1rem 0;
        animation: fadeInDown 0.6s ease-in;
    }
    
    /* Page Title Animation */
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Enhanced Metric Cards */
    .stMetric {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .stMetric:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(102, 126, 234, 0.4);
    }
    
    .stMetric label {
        color: white !important;
        font-weight: 600;
        font-size: 0.95rem;
    }
    
    .stMetric .metric-value {
        color: white !important;
        font-size: 2rem;
        font-weight: 700;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] .css-1d391kg {
        background: transparent;
    }
    
    /* Enhanced Buttons - Override Streamlit defaults */
    .stButton > button,
    .stButton > button:focus,
    .stButton > button:active,
    .stButton > button:hover,
    button[kind="primary"],
    button[kind="secondary"],
    div[data-testid="stForm"] button,
    [class*="stButton"] button {
        background-color: #667eea !important;
        background-image: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 600 !important;
        width: 100%;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1) !important;
    }
    
    .stButton > button p,
    button[kind="primary"] p,
    button[kind="secondary"] p {
        color: #ffffff !important;
    }
    
    .stButton > button:hover,
    button[kind="primary"]:hover,
    button[kind="secondary"]:hover {
        background-color: #5568d3 !important;
        background-image: linear-gradient(135deg, #5568d3 0%, #6a3f8f 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 15px rgba(0,0,0,0.2) !important;
        color: #ffffff !important;
    }
    
    /* Form Styling */
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stSelectbox>div>div>select,
    .stTextArea>div>div>textarea {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 0.6rem;
        transition: border-color 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus,
    .stNumberInput>div>div>input:focus,
    .stSelectbox>div>div>select:focus,
    .stTextArea>div>div>textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
    }
    
    /* DataFrames */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Info/Success/Warning/Error Messages */
    .stAlert {
        border-radius: 10px;
        padding: 1rem 1.5rem;
        border-left: 4px solid;
        animation: slideInLeft 0.4s ease;
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Pulse Glow Animation for Success Messages */
    .success-pulse {
        animation: pulseGlow 1.5s ease-in-out;
    }
    
    @keyframes pulseGlow {
        0% {
            opacity: 0;
            transform: scale(0.95);
            box-shadow: 0 0 0 rgba(16, 185, 129, 0);
        }
        50% {
            opacity: 1;
            transform: scale(1.02);
            box-shadow: 0 0 20px rgba(16, 185, 129, 0.6);
        }
        100% {
            opacity: 1;
            transform: scale(1);
            box-shadow: 0 0 0 rgba(16, 185, 129, 0);
        }
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px 10px 0 0 !important;
        padding: 0.8rem 1.5rem !important;
        font-weight: 600 !important;
        background-color: #f0f2f6 !important;
        color: #333333 !important;
        transition: all 0.3s ease !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        background-color: #667eea !important;
        color: #ffffff !important;
    }
    
    .stTabs [aria-selected="true"] button,
    .stTabs [aria-selected="true"] div {
        color: #ffffff !important;
    }
    
    /* Chat Messages */
    .stChatMessage {
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        animation: fadeIn 0.4s ease;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Chat Input */
    .stChatInput>div>div>input {
        border-radius: 25px;
        padding: 0.8rem 1.5rem;
        border: 2px solid #e0e0e0;
        transition: all 0.3s ease;
    }
    
    .stChatInput>div>div>input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
    }
    
    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #5568d3 0%, #6a3f8f 100%);
    }
    
    /* Card-like containers */
    .element-container {
        transition: all 0.3s ease;
    }
    
    /* Plotly charts */
    .js-plotly-plot {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Improve readability */
    body {
        font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }
    
    /* Subheader styling */
    .stMarkdown h2 {
        color: #667eea;
        border-bottom: 3px solid #667eea;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
    }
    
    .stMarkdown h3 {
        color: #764ba2;
        margin-top: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'dashboard'

def main():
    """
    Main application function
    """
    # Sidebar navigation
    with st.sidebar:
        # Hospital Logo and Title with better styling
        st.markdown("""
        <div style='text-align: center; padding: 1.5rem 0;'>
            <h1 style='color: white; font-size: 2rem; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);'>
                🏥 Smart Hospital
            </h1>
            <p style='color: rgba(255,255,255,0.8); font-size: 0.9rem; margin-top: 0.5rem;'>
                Intelligent Healthcare Management
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<hr style='margin: 1rem 0; border-color: rgba(255,255,255,0.2);'>", unsafe_allow_html=True)
        
        st.markdown("<p style='color: rgba(255,255,255,0.9); font-weight: 600; margin-bottom: 0.8rem; padding-left: 0.5rem;'>📍 NAVIGATION</p>", unsafe_allow_html=True)
        
        # Navigation buttons with improved styling
        pages = {
            "🏠 Dashboard": "dashboard",
            "👥 Patients": "patients",
            "👩‍⚕️ Doctors": "doctors",
            "📅 Appointments": "appointments",
            "🤖 AI Prediction": "prediction",
            "💬 AI Chatbot": "chatbot"
        }
        
        for page_name, page_key in pages.items():
            # Highlight current page
            is_current = st.session_state.current_page == page_key
            button_type = "primary" if is_current else "secondary"
            
            if st.button(page_name, key=page_key, use_container_width=True, type=button_type if is_current else "secondary"):
                st.session_state.current_page = page_key
                st.rerun()
        
        st.markdown("<hr style='margin: 2rem 0; border-color: rgba(255,255,255,0.2);'>", unsafe_allow_html=True)
        
        # Footer with better styling
        st.markdown("""
        <div style='text-align: center; color: rgba(255,255,255,0.8); font-size: 0.85rem;'>
            <p style='margin: 0.3rem 0;'><strong>👨‍💻 Developed by:</strong></p>
            <p style='margin: 0.3rem 0;'>Krishna + Omkar</p>
        </div>
        """, unsafe_allow_html=True)
    
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
    elif st.session_state.current_page == 'chatbot':
        chatbot_page()

# =====================================================
# DASHBOARD PAGE
# =====================================================

def dashboard_page():
    """
    Hospital dashboard with analytics and overview
    """
    st.markdown("<h1 class='main-header'>🏥 Hospital Dashboard</h1>", unsafe_allow_html=True)
    
    # Welcome message with current date
    from datetime import datetime
    current_date = datetime.now().strftime("%B %d, %Y")
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
                padding: 1rem;
                border-radius: 10px;
                margin-bottom: 2rem;
                text-align: center;'>
        <p style='margin: 0; color: #667eea; font-size: 1.1rem; font-weight: 600;'>
            Welcome to Smart Hospital Management System
        </p>
        <p style='margin: 0.3rem 0 0 0; color: #666; font-size: 0.9rem;'>
            {current_date}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        # Get dashboard statistics
        stats = db.get_dashboard_stats()
        
        # Key metrics row with enhanced styling
        st.markdown("### 📊 Key Metrics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="👥 Total Patients",
                value=stats['total_patients'],
                delta=f"+{stats['total_patients'] - 5} this month" if stats['total_patients'] > 5 else "New system"
            )
        
        with col2:
            st.metric(
                label="👩‍⚕️ Total Doctors",
                value=stats['total_doctors'],
                delta=f"{stats['total_doctors']} active"
            )
        
        with col3:
            st.metric(
                label="📅 Scheduled",
                value=stats['scheduled_appointments'],
                delta=f"{stats['scheduled_appointments']} upcoming"
            )
        
        with col4:
            st.metric(
                label="📊 Today's Visits",
                value=stats['todays_visits'],
                delta=f"{stats['todays_visits']} today"
            )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Charts row with section header
        st.markdown("### 📊 Analytics & Insights")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📅 Upcoming Appointments")
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
            st.markdown("#### 🔍 Top Predicted Diseases")
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
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 📋 Recent Activity")
        
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
                        st.markdown("""
                        <div class='success-pulse' style='background: #d4edda; border-left: 4px solid #28a745; 
                             padding: 1rem; border-radius: 10px; color: #155724;'>
                            <strong>✅ Patient '{name}' added successfully!</strong><br>
                            Patient ID: {patient_id}
                        </div>
                        """.format(name=name, patient_id=patient_id), unsafe_allow_html=True)
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
                        st.markdown("""
                        <div class='success-pulse' style='background: #d4edda; border-left: 4px solid #28a745; 
                             padding: 1rem; border-radius: 10px; color: #155724;'>
                            <strong>✅ Doctor '{name}' added successfully!</strong><br>
                            Doctor ID: {doctor_id}
                        </div>
                        """.format(name=name, doctor_id=doctor_id), unsafe_allow_html=True)
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
                                
                                st.markdown("""
                                <div class='success-pulse' style='background: #d4edda; border-left: 4px solid #28a745; 
                                     padding: 1rem; border-radius: 10px; color: #155724;'>
                                    <strong>✅ Appointment scheduled successfully!</strong><br>
                                    Appointment ID: {appointment_id}
                                </div>
                                """.format(appointment_id=appointment_id), unsafe_allow_html=True)
                                
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
            # Get all appointments, then filter for Scheduled ones
            all_appointments = db.get_appointments()
            if all_appointments:
                appointments = [a for a in all_appointments if a.get('status') == 'Scheduled']
            else:
                appointments = []
            
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

# =====================================================
# CHATBOT PAGE
# =====================================================

def chatbot_page():
    """
    AI Chatbot interface for conversational disease prediction
    """
    st.markdown("<h1 class='main-header'>💬 AI Medical Chatbot</h1>", unsafe_allow_html=True)
    
    # Import chatbot module
    try:
        from chatbot import get_chatbot, reset_chatbot
        chatbot_available = True
    except Exception as e:
        st.error(f"❌ Chatbot module loading failed: {e}")
        chatbot_available = False
        return
    
    # Initialize session state for chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
        st.session_state.chatbot_started = False
    
    # Enhanced info banner with gradient
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
                border-left: 4px solid #667eea;
                padding: 1.2rem;
                border-radius: 10px;
                margin-bottom: 1.5rem;'>
        <p style='margin: 0; color: #333; font-size: 1rem;'>
            <strong>💡 How it works:</strong> This AI chatbot will ask you questions about your symptoms 
            and medical history to provide an intelligent disease prediction. Just chat naturally!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Control buttons with better layout
    col1, col2, col3, col4 = st.columns([1.5, 1.5, 1.5, 3.5])
    with col1:
        if st.button("🆕 New Chat", type="primary", use_container_width=True):
            reset_chatbot()
            st.session_state.chat_history = []
            st.session_state.chatbot_started = False
            st.rerun()
    
    with col2:
        show_help = st.button("ℹ️ Help", use_container_width=True)
    
    with col3:
        if len(st.session_state.chat_history) > 0:
            if st.button("📋 Export Chat", use_container_width=True):
                # Export chat history
                chat_text = "\n\n".join([
                    f"{'User' if msg['role'] == 'user' else 'Bot'}: {msg['message']}" 
                    for msg in st.session_state.chat_history
                ])
                st.download_button(
                    label="📥 Download",
                    data=chat_text,
                    file_name="chat_history.txt",
                    mime="text/plain",
                    use_container_width=True
                )
    
    if show_help:
        st.markdown("""
        <div style='background: #f8f9fa; padding: 1.5rem; border-radius: 10px; margin: 1rem 0;'>
            <h4 style='color: #667eea; margin-top: 0;'>💬 Chat Commands</h4>
            <ul style='margin: 0.5rem 0;'>
                <li>Type <code>restart</code> to start over</li>
                <li>Type <code>quit</code> to end conversation</li>
                <li>Answer questions naturally</li>
            </ul>
            <h4 style='color: #667eea; margin-top: 1rem;'>📝 Example Responses</h4>
            <ul style='margin: 0.5rem 0;'>
                <li><code>'John, 35, Male'</code> - for patient info</li>
                <li><code>'I have a headache and fever'</code> - for symptoms</li>
                <li><code>'Yes'</code> or <code>'No'</code> - for yes/no questions</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Chat container
    st.markdown("---")
    
    # Display chat history
    chat_container = st.container()
    
    with chat_container:
        if not st.session_state.chatbot_started:
            # Show initial greeting
            chatbot = get_chatbot()
            greeting = chatbot.start_conversation()
            st.session_state.chat_history.append({
                'role': 'assistant',
                'message': greeting
            })
            st.session_state.chatbot_started = True
        
        # Display all messages
        for i, chat in enumerate(st.session_state.chat_history):
            if chat['role'] == 'user':
                with st.chat_message("user", avatar="👤"):
                    st.markdown(chat['message'])
            else:
                with st.chat_message("assistant", avatar="🤖"):
                    st.markdown(chat['message'])
    
    # Chat input
    user_input = st.chat_input("Type your message here...")
    
    if user_input:
        # Add user message to history
        st.session_state.chat_history.append({
            'role': 'user',
            'message': user_input
        })
        
        # Get chatbot response
        chatbot = get_chatbot()
        response = chatbot.process_message(user_input)
        
        # Check if chatbot generated a prediction
        if chatbot.conversation_state == "completed":
            # Save prediction to database if possible
            try:
                collected_data = chatbot.get_collected_data()
                patient_info = collected_data['patient_info']
                symptoms = collected_data['symptoms']
                
                # Get the prediction from the response
                # Extract the top disease from response
                if "**AI Prediction Results**" in response:
                    # Try to parse the top prediction
                    lines = response.split('\n')
                    for line in lines:
                        if line.strip().startswith('1.'):
                            # Extract disease name and confidence
                            import re
                            match = re.search(r'\*\*(.+?)\*\* - ([\d.]+)%', line)
                            if match:
                                predicted_disease = match.group(1)
                                confidence = float(match.group(2)) / 100
                                
                                # Build symptoms text
                                symptom_list = [k.replace('_', ' ') for k, v in symptoms.items() 
                                              if v == 1 and k in chatbot.all_symptoms]
                                symptoms_text = ", ".join(symptom_list)
                                
                                # Try to find existing patient or create new one
                                patient_name = patient_info.get('name', 'Patient')
                                patient_age = patient_info.get('age', 30)
                                patient_gender = patient_info.get('gender', 'Other')
                                
                                # Search for existing patient by name
                                patients = db.get_patients()
                                existing_patient = None
                                for p in patients:
                                    if p['name'].lower() == patient_name.lower():
                                        existing_patient = p
                                        break
                                
                                if existing_patient:
                                    patient_id = existing_patient['patient_id']
                                else:
                                    # Create new patient
                                    patient_id = db.add_patient(patient_name, patient_age, patient_gender)
                                
                                # Save prediction
                                record_id = db.save_prediction(
                                    patient_id=patient_id,
                                    predicted_disease=predicted_disease,
                                    confidence_score=confidence,
                                    symptoms=symptoms_text
                                )
                                
                                response += f"\n\n✅ **Prediction saved to medical records!** (Record ID: {record_id})"
                                break
            except Exception as e:
                st.warning(f"Note: Could not save prediction to database: {e}")
        
        # Add assistant response to history
        st.session_state.chat_history.append({
            'role': 'assistant',
            'message': response
        })
        
        # Rerun to update display
        st.rerun()
    
    # Sidebar with chat statistics
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 📊 Chat Stats")
        st.metric("Messages", len(st.session_state.chat_history))
        
        if st.session_state.chat_history:
            chatbot = get_chatbot()
            if chatbot.conversation_state != "greeting":
                collected_data = chatbot.get_collected_data()
                symptoms = collected_data.get('symptoms', {})
                symptom_count = sum(1 for v in symptoms.values() if v == 1)
                st.metric("Symptoms Collected", symptom_count)
                st.metric("Conversation State", chatbot.conversation_state.replace('_', ' ').title())

if __name__ == "__main__":
    main()
