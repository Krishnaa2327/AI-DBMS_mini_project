#!/usr/bin/env python3
"""
Smart Hospital Management System - Database Connection Module
Created by: Krishna + Omkar
Date: October 12, 2025
Phase: 2 - Database Integration

This module provides comprehensive CRUD operations for all database tables.
"""

import mysql.connector
from mysql.connector import Error, pooling
from datetime import datetime, date
from typing import List, Dict, Optional, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HospitalDatabase:
    """
    Hospital Management System Database Interface
    Provides CRUD operations for all tables
    """
    
    def __init__(self, host="localhost", user="root", password="Krishna@112406", database="smart_hospital"):
        """
        Initialize database connection
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        
        # Connection pool for better performance
        self.pool_config = {
            'pool_name': 'hospital_pool',
            'pool_size': 5,
            'pool_reset_session': True,
            'host': host,
            'user': user,
            'password': password,
            'database': database
        }
        
        try:
            self.pool = mysql.connector.pooling.MySQLConnectionPool(**self.pool_config)
            logger.info("✅ Database connection pool created successfully")
        except Error as e:
            logger.error(f"❌ Error creating connection pool: {e}")
            raise
    
    def get_connection(self):
        """
        Get connection from pool
        """
        try:
            return self.pool.get_connection()
        except Error as e:
            logger.error(f"❌ Error getting connection: {e}")
            raise
    
    def test_connection(self) -> bool:
        """
        Test database connection
        """
        try:
            conn = self.get_connection()
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                cursor.fetchone()
                cursor.close()
                conn.close()
                logger.info("✅ Database connection test successful")
                return True
        except Error as e:
            logger.error(f"❌ Database connection test failed: {e}")
            return False
    
    # =====================================================
    # PATIENT OPERATIONS
    # =====================================================
    
    def add_patient(self, name: str, age: int, gender: str, contact: str = None, address: str = None) -> int:
        """
        Add new patient
        Returns: patient_id
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            query = """
            INSERT INTO patients (name, age, gender, contact, address)
            VALUES (%s, %s, %s, %s, %s)
            """
            
            cursor.execute(query, (name, age, gender, contact, address))
            conn.commit()
            patient_id = cursor.lastrowid
            
            cursor.close()
            conn.close()
            
            logger.info(f"✅ Patient added successfully: ID {patient_id}")
            return patient_id
            
        except Error as e:
            logger.error(f"❌ Error adding patient: {e}")
            raise
    
    def get_patients(self, limit: int = 100) -> List[Dict]:
        """
        Get all patients
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = "SELECT * FROM patients ORDER BY created_at DESC LIMIT %s"
            cursor.execute(query, (limit,))
            patients = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return patients
            
        except Error as e:
            logger.error(f"❌ Error fetching patients: {e}")
            raise
    
    def get_patient_by_id(self, patient_id: int) -> Optional[Dict]:
        """
        Get patient by ID
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = "SELECT * FROM patients WHERE patient_id = %s"
            cursor.execute(query, (patient_id,))
            patient = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            return patient
            
        except Error as e:
            logger.error(f"❌ Error fetching patient: {e}")
            raise
    
    def update_patient(self, patient_id: int, **kwargs) -> bool:
        """
        Update patient information
        """
        try:
            if not kwargs:
                return False
            
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Build dynamic update query
            set_clause = ", ".join([f"{key} = %s" for key in kwargs.keys()])
            query = f"UPDATE patients SET {set_clause} WHERE patient_id = %s"
            
            values = list(kwargs.values()) + [patient_id]
            cursor.execute(query, values)
            conn.commit()
            
            affected_rows = cursor.rowcount
            cursor.close()
            conn.close()
            
            if affected_rows > 0:
                logger.info(f"✅ Patient {patient_id} updated successfully")
                return True
            else:
                logger.warning(f"⚠️ No patient found with ID {patient_id}")
                return False
                
        except Error as e:
            logger.error(f"❌ Error updating patient: {e}")
            raise
    
    # =====================================================
    # DOCTOR OPERATIONS
    # =====================================================
    
    def add_doctor(self, name: str, specialization: str, contact: str = None, email: str = None) -> int:
        """
        Add new doctor
        Returns: doctor_id
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            query = """
            INSERT INTO doctors (name, specialization, contact, email)
            VALUES (%s, %s, %s, %s)
            """
            
            cursor.execute(query, (name, specialization, contact, email))
            conn.commit()
            doctor_id = cursor.lastrowid
            
            cursor.close()
            conn.close()
            
            logger.info(f"✅ Doctor added successfully: ID {doctor_id}")
            return doctor_id
            
        except Error as e:
            logger.error(f"❌ Error adding doctor: {e}")
            raise
    
    def get_doctors(self, specialization: str = None) -> List[Dict]:
        """
        Get all doctors or filter by specialization
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            if specialization:
                query = "SELECT * FROM doctors WHERE specialization = %s ORDER BY name"
                cursor.execute(query, (specialization,))
            else:
                query = "SELECT * FROM doctors ORDER BY name"
                cursor.execute(query)
            
            doctors = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return doctors
            
        except Error as e:
            logger.error(f"❌ Error fetching doctors: {e}")
            raise
    
    def get_doctor_by_id(self, doctor_id: int) -> Optional[Dict]:
        """
        Get doctor by ID
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = "SELECT * FROM doctors WHERE doctor_id = %s"
            cursor.execute(query, (doctor_id,))
            doctor = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            return doctor
            
        except Error as e:
            logger.error(f"❌ Error fetching doctor: {e}")
            raise
    
    # =====================================================
    # APPOINTMENT OPERATIONS
    # =====================================================
    
    def schedule_appointment(self, patient_id: int, doctor_id: int, appointment_date: datetime, 
                           notes: str = None) -> int:
        """
        Schedule new appointment
        Returns: appointment_id
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            query = """
            INSERT INTO appointments (patient_id, doctor_id, appointment_date, notes)
            VALUES (%s, %s, %s, %s)
            """
            
            cursor.execute(query, (patient_id, doctor_id, appointment_date, notes))
            conn.commit()
            appointment_id = cursor.lastrowid
            
            cursor.close()
            conn.close()
            
            logger.info(f"✅ Appointment scheduled successfully: ID {appointment_id}")
            return appointment_id
            
        except Error as e:
            logger.error(f"❌ Error scheduling appointment: {e}")
            raise
    
    def get_appointments(self, status: str = None, date_from: date = None, date_to: date = None) -> List[Dict]:
        """
        Get appointments with optional filters
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = """
            SELECT a.*, p.name as patient_name, d.name as doctor_name, d.specialization
            FROM appointments a
            JOIN patients p ON a.patient_id = p.patient_id
            JOIN doctors d ON a.doctor_id = d.doctor_id
            WHERE 1=1
            """
            
            params = []
            
            if status:
                query += " AND a.status = %s"
                params.append(status)
            
            if date_from:
                query += " AND DATE(a.appointment_date) >= %s"
                params.append(date_from)
            
            if date_to:
                query += " AND DATE(a.appointment_date) <= %s"
                params.append(date_to)
            
            query += " ORDER BY a.appointment_date"
            
            cursor.execute(query, params)
            appointments = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return appointments
            
        except Error as e:
            logger.error(f"❌ Error fetching appointments: {e}")
            raise
    
    def update_appointment_status(self, appointment_id: int, status: str) -> bool:
        """
        Update appointment status
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            query = "UPDATE appointments SET status = %s WHERE appointment_id = %s"
            cursor.execute(query, (status, appointment_id))
            conn.commit()
            
            affected_rows = cursor.rowcount
            cursor.close()
            conn.close()
            
            if affected_rows > 0:
                logger.info(f"✅ Appointment {appointment_id} status updated to {status}")
                return True
            else:
                logger.warning(f"⚠️ No appointment found with ID {appointment_id}")
                return False
                
        except Error as e:
            logger.error(f"❌ Error updating appointment status: {e}")
            raise
    
    # =====================================================
    # MEDICAL RECORDS OPERATIONS
    # =====================================================
    
    def save_medical_record(self, patient_id: int, doctor_id: int, appointment_id: int = None,
                          symptoms: str = None, diagnosis: str = None, predicted_disease: str = None,
                          confidence_score: float = None, medicines: str = None, 
                          treatment_notes: str = None, follow_up_date: date = None) -> int:
        """
        Save medical record
        Returns: record_id
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            query = """
            INSERT INTO medical_records 
            (patient_id, doctor_id, appointment_id, symptoms, diagnosis, predicted_disease, 
             confidence_score, medicines, treatment_notes, follow_up_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(query, (patient_id, doctor_id, appointment_id, symptoms, diagnosis,
                                 predicted_disease, confidence_score, medicines, treatment_notes,
                                 follow_up_date))
            conn.commit()
            record_id = cursor.lastrowid
            
            cursor.close()
            conn.close()
            
            logger.info(f"✅ Medical record saved successfully: ID {record_id}")
            return record_id
            
        except Error as e:
            logger.error(f"❌ Error saving medical record: {e}")
            raise
    
    def get_patient_history(self, patient_id: int) -> List[Dict]:
        """
        Get patient's medical history
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = """
            SELECT mr.*, d.name as doctor_name, d.specialization
            FROM medical_records mr
            JOIN doctors d ON mr.doctor_id = d.doctor_id
            WHERE mr.patient_id = %s
            ORDER BY mr.visit_date DESC
            """
            
            cursor.execute(query, (patient_id,))
            history = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return history
            
        except Error as e:
            logger.error(f"❌ Error fetching patient history: {e}")
            raise
    
    def save_prediction(self, patient_id: int, predicted_disease: str, confidence_score: float,
                       symptoms: str = None) -> int:
        """
        Save ML prediction (simplified medical record)
        Returns: record_id
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Use a default "AI Doctor" - you might want to create this doctor in your system
            query = """
            INSERT INTO medical_records 
            (patient_id, doctor_id, symptoms, predicted_disease, confidence_score)
            VALUES (%s, 1, %s, %s, %s)
            """
            
            cursor.execute(query, (patient_id, symptoms, predicted_disease, confidence_score))
            conn.commit()
            record_id = cursor.lastrowid
            
            cursor.close()
            conn.close()
            
            logger.info(f"✅ ML prediction saved successfully: ID {record_id}")
            return record_id
            
        except Error as e:
            logger.error(f"❌ Error saving prediction: {e}")
            raise
    
    # =====================================================
    # ANALYTICS & DASHBOARD QUERIES
    # =====================================================
    
    def get_dashboard_stats(self) -> Dict:
        """
        Get dashboard statistics
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            stats = {}
            
            # Total counts
            cursor.execute("SELECT COUNT(*) as count FROM patients")
            stats['total_patients'] = cursor.fetchone()['count']
            
            cursor.execute("SELECT COUNT(*) as count FROM doctors")
            stats['total_doctors'] = cursor.fetchone()['count']
            
            cursor.execute("SELECT COUNT(*) as count FROM appointments WHERE status = 'Scheduled'")
            stats['scheduled_appointments'] = cursor.fetchone()['count']
            
            cursor.execute("SELECT COUNT(*) as count FROM medical_records WHERE DATE(visit_date) = CURDATE()")
            stats['todays_visits'] = cursor.fetchone()['count']
            
            # Recent appointments
            cursor.execute("""
                SELECT a.appointment_date, p.name as patient_name, d.name as doctor_name
                FROM appointments a
                JOIN patients p ON a.patient_id = p.patient_id
                JOIN doctors d ON a.doctor_id = d.doctor_id
                WHERE a.appointment_date >= NOW()
                ORDER BY a.appointment_date LIMIT 5
            """)
            stats['upcoming_appointments'] = cursor.fetchall()
            
            # Disease predictions summary
            cursor.execute("""
                SELECT predicted_disease, COUNT(*) as count
                FROM medical_records 
                WHERE predicted_disease IS NOT NULL
                GROUP BY predicted_disease
                ORDER BY count DESC LIMIT 5
            """)
            stats['top_predicted_diseases'] = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return stats
            
        except Error as e:
            logger.error(f"❌ Error fetching dashboard stats: {e}")
            raise

# =====================================================
# GLOBAL DATABASE INSTANCE
# =====================================================

# Create global database instance
db = HospitalDatabase()

# Test connection on import
if __name__ == "__main__":
    if db.test_connection():
        print("🏥 Hospital Database Module loaded successfully!")
        
        # Quick test
        stats = db.get_dashboard_stats()
        print(f"📊 Dashboard Stats: {stats['total_patients']} patients, {stats['total_doctors']} doctors")
    else:
        print("❌ Database connection failed!")