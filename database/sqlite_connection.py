#!/usr/bin/env python3
"""
Smart Hospital Management System - SQLite Database Connection Module
Created for Streamlit Cloud Deployment
Date: October 20, 2025

This module provides the same interface as the MySQL version but uses SQLite
for deployment compatibility.
"""

import sqlite3
import os
from datetime import datetime, date
from typing import List, Dict, Optional, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HospitalDatabase:
    """
    Hospital Management System Database Interface - SQLite Version
    Provides CRUD operations for all tables
    """
    
    def __init__(self, db_path: str = "hospital.db"):
        """
        Initialize SQLite database connection
        """
        self.db_path = db_path
        self.init_database()
        
    def init_database(self):
        """
        Initialize database tables
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Create tables
            cursor.executescript("""
                CREATE TABLE IF NOT EXISTS patients (
                    patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    gender TEXT NOT NULL,
                    contact TEXT,
                    address TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
                CREATE TABLE IF NOT EXISTS doctors (
                    doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    specialization TEXT NOT NULL,
                    contact TEXT,
                    email TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
                CREATE TABLE IF NOT EXISTS appointments (
                    appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id INTEGER NOT NULL,
                    doctor_id INTEGER NOT NULL,
                    appointment_date TIMESTAMP NOT NULL,
                    status TEXT DEFAULT 'Scheduled',
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
                    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
                );
                
                CREATE TABLE IF NOT EXISTS medical_records (
                    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id INTEGER NOT NULL,
                    predicted_disease TEXT,
                    confidence_score REAL,
                    symptoms TEXT,
                    visit_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
                );
            """)
            
            conn.commit()
            cursor.close()
            conn.close()
            
            logger.info("✅ SQLite database initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Error initializing database: {e}")
            raise
    
    def get_connection(self):
        """
        Get SQLite connection
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Enable dict-like access
            return conn
        except Exception as e:
            logger.error(f"❌ Error getting connection: {e}")
            raise
    
    def test_connection(self) -> bool:
        """
        Test database connection
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            cursor.close()
            conn.close()
            logger.info("✅ Database connection test successful")
            return True
        except Exception as e:
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
            
            cursor.execute("""
                INSERT INTO patients (name, age, gender, contact, address)
                VALUES (?, ?, ?, ?, ?)
            """, (name, age, gender, contact, address))
            
            patient_id = cursor.lastrowid
            conn.commit()
            cursor.close()
            conn.close()
            
            logger.info(f"✅ Patient added successfully: ID {patient_id}")
            return patient_id
            
        except Exception as e:
            logger.error(f"❌ Error adding patient: {e}")
            raise
    
    def get_patients(self, limit: int = 100) -> List[Dict]:
        """
        Get all patients
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM patients ORDER BY created_at DESC LIMIT ?", (limit,))
            rows = cursor.fetchall()
            patients = [dict(row) for row in rows]
            
            cursor.close()
            conn.close()
            
            return patients
            
        except Exception as e:
            logger.error(f"❌ Error fetching patients: {e}")
            raise
    
    def get_patient_by_id(self, patient_id: int) -> Optional[Dict]:
        """
        Get patient by ID
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM patients WHERE patient_id = ?", (patient_id,))
            row = cursor.fetchone()
            patient = dict(row) if row else None
            
            cursor.close()
            conn.close()
            
            return patient
            
        except Exception as e:
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
            set_clause = ", ".join([f"{key} = ?" for key in kwargs.keys()])
            query = f"UPDATE patients SET {set_clause} WHERE patient_id = ?"
            
            values = list(kwargs.values()) + [patient_id]
            cursor.execute(query, values)
            
            affected_rows = cursor.rowcount
            conn.commit()
            cursor.close()
            conn.close()
            
            if affected_rows > 0:
                logger.info(f"✅ Patient {patient_id} updated successfully")
                return True
            else:
                logger.warning(f"⚠️ No patient found with ID {patient_id}")
                return False
                
        except Exception as e:
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
            
            cursor.execute("""
                INSERT INTO doctors (name, specialization, contact, email)
                VALUES (?, ?, ?, ?)
            """, (name, specialization, contact, email))
            
            doctor_id = cursor.lastrowid
            conn.commit()
            cursor.close()
            conn.close()
            
            logger.info(f"✅ Doctor added successfully: ID {doctor_id}")
            return doctor_id
            
        except Exception as e:
            logger.error(f"❌ Error adding doctor: {e}")
            raise
    
    def get_doctors(self, limit: int = 100) -> List[Dict]:
        """
        Get all doctors
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM doctors ORDER BY created_at DESC LIMIT ?", (limit,))
            rows = cursor.fetchall()
            doctors = [dict(row) for row in rows]
            
            cursor.close()
            conn.close()
            
            return doctors
            
        except Exception as e:
            logger.error(f"❌ Error fetching doctors: {e}")
            raise
    
    # =====================================================
    # APPOINTMENT OPERATIONS
    # =====================================================
    
    def schedule_appointment(self, patient_id: int, doctor_id: int, appointment_date: datetime, notes: str = None) -> int:
        """
        Schedule new appointment
        Returns: appointment_id
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO appointments (patient_id, doctor_id, appointment_date, notes)
                VALUES (?, ?, ?, ?)
            """, (patient_id, doctor_id, appointment_date, notes))
            
            appointment_id = cursor.lastrowid
            conn.commit()
            cursor.close()
            conn.close()
            
            logger.info(f"✅ Appointment scheduled successfully: ID {appointment_id}")
            return appointment_id
            
        except Exception as e:
            logger.error(f"❌ Error scheduling appointment: {e}")
            raise
    
    def get_appointments(self, status: str = None, date_from: date = None, date_to: date = None, limit: int = 100) -> List[Dict]:
        """
        Get appointments with filters
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            query = """
                SELECT a.*, p.name as patient_name, d.name as doctor_name, d.specialization
                FROM appointments a
                JOIN patients p ON a.patient_id = p.patient_id
                JOIN doctors d ON a.doctor_id = d.doctor_id
                WHERE 1=1
            """
            params = []
            
            if status:
                query += " AND a.status = ?"
                params.append(status)
            
            if date_from:
                query += " AND DATE(a.appointment_date) >= ?"
                params.append(date_from.strftime('%Y-%m-%d'))
            
            if date_to:
                query += " AND DATE(a.appointment_date) <= ?"
                params.append(date_to.strftime('%Y-%m-%d'))
            
            query += " ORDER BY a.appointment_date DESC LIMIT ?"
            params.append(limit)
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            appointments = [dict(row) for row in rows]
            
            cursor.close()
            conn.close()
            
            return appointments
            
        except Exception as e:
            logger.error(f"❌ Error fetching appointments: {e}")
            raise
    
    def update_appointment_status(self, appointment_id: int, status: str) -> bool:
        """
        Update appointment status
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE appointments 
                SET status = ? 
                WHERE appointment_id = ?
            """, (status, appointment_id))
            
            affected_rows = cursor.rowcount
            conn.commit()
            cursor.close()
            conn.close()
            
            if affected_rows > 0:
                logger.info(f"✅ Appointment {appointment_id} status updated to {status}")
                return True
            else:
                logger.warning(f"⚠️ No appointment found with ID {appointment_id}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error updating appointment status: {e}")
            raise
    
    # =====================================================
    # MEDICAL RECORDS OPERATIONS
    # =====================================================
    
    def save_prediction(self, patient_id: int, predicted_disease: str, confidence_score: float, symptoms: str) -> int:
        """
        Save AI prediction to medical records
        Returns: record_id
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO medical_records (patient_id, predicted_disease, confidence_score, symptoms)
                VALUES (?, ?, ?, ?)
            """, (patient_id, predicted_disease, confidence_score, symptoms))
            
            record_id = cursor.lastrowid
            conn.commit()
            cursor.close()
            conn.close()
            
            logger.info(f"✅ Prediction saved successfully: Record ID {record_id}")
            return record_id
            
        except Exception as e:
            logger.error(f"❌ Error saving prediction: {e}")
            raise
    
    # =====================================================
    # DASHBOARD STATISTICS
    # =====================================================
    
    def get_dashboard_stats(self) -> Dict:
        """
        Get dashboard statistics
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Basic counts
            cursor.execute("SELECT COUNT(*) FROM patients")
            total_patients = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM doctors")
            total_doctors = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM appointments WHERE status = 'Scheduled'")
            scheduled_appointments = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM appointments WHERE DATE(appointment_date) = DATE('now')")
            todays_visits = cursor.fetchone()[0]
            
            # Upcoming appointments
            cursor.execute("""
                SELECT a.appointment_date, p.name as patient_name, d.name as doctor_name
                FROM appointments a
                JOIN patients p ON a.patient_id = p.patient_id
                JOIN doctors d ON a.doctor_id = d.doctor_id
                WHERE a.status = 'Scheduled' AND a.appointment_date >= datetime('now')
                ORDER BY a.appointment_date LIMIT 5
            """)
            upcoming_appointments = [dict(row) for row in cursor.fetchall()]
            
            # Top predicted diseases
            cursor.execute("""
                SELECT predicted_disease, COUNT(*) as count
                FROM medical_records 
                WHERE predicted_disease IS NOT NULL
                GROUP BY predicted_disease
                ORDER BY count DESC LIMIT 5
            """)
            top_predicted_diseases = [dict(row) for row in cursor.fetchall()]
            
            cursor.close()
            conn.close()
            
            return {
                'total_patients': total_patients,
                'total_doctors': total_doctors,
                'scheduled_appointments': scheduled_appointments,
                'todays_visits': todays_visits,
                'upcoming_appointments': upcoming_appointments,
                'top_predicted_diseases': top_predicted_diseases
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting dashboard stats: {e}")
            return {
                'total_patients': 0,
                'total_doctors': 0,
                'scheduled_appointments': 0,
                'todays_visits': 0,
                'upcoming_appointments': [],
                'top_predicted_diseases': []
            }

# =====================================================
# GLOBAL DATABASE INSTANCE
# =====================================================

# Create global database instance
db = HospitalDatabase()

# Test connection on import
if __name__ == "__main__":
    if db.test_connection():
        print("✅ SQLite database connection successful")
    else:
        print("❌ SQLite database connection failed")