-- =====================================================
-- Smart Hospital Management System - Database Setup
-- Created by: Krishna + Omkar
-- Date: October 12, 2025
-- Phase: 2 - Database Integration
-- =====================================================

-- Step 1: Create database (if not exists)
CREATE DATABASE IF NOT EXISTS smart_hospital;
USE smart_hospital;

-- Step 2: Drop existing tables (for clean setup)
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS medical_records;
DROP TABLE IF EXISTS appointments;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS patients;
DROP TABLE IF EXISTS doctors;
SET FOREIGN_KEY_CHECKS = 1;

-- Step 3: Create all tables (execute schema.sql content)
-- 1. PATIENTS TABLE - Enhanced with address field
CREATE TABLE patients (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT CHECK (age > 0 AND age <= 150),
    gender ENUM('Male', 'Female', 'Other') NOT NULL,
    contact VARCHAR(15),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 2. DOCTORS TABLE - Enhanced with email field
CREATE TABLE doctors (
    doctor_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    specialization VARCHAR(100) NOT NULL,
    contact VARCHAR(15),
    email VARCHAR(100) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 3. APPOINTMENTS TABLE - Enhanced with status enum
CREATE TABLE appointments (
    appointment_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    appointment_date DATETIME NOT NULL,
    status ENUM('Scheduled', 'Completed', 'Cancelled') DEFAULT 'Scheduled',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE
);

-- 4. MEDICAL RECORDS TABLE - Comprehensive medical data storage
CREATE TABLE medical_records (
    record_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    appointment_id INT,
    symptoms TEXT,
    diagnosis TEXT,
    predicted_disease VARCHAR(100),
    confidence_score FLOAT CHECK (confidence_score >= 0 AND confidence_score <= 1),
    medicines TEXT,
    treatment_notes TEXT,
    visit_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    follow_up_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE,
    FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id) ON DELETE SET NULL
);

-- 5. USERS TABLE - Authentication system
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('Doctor', 'Admin', 'Receptionist') NOT NULL,
    email VARCHAR(100) UNIQUE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Step 4: Create indexes for performance
-- Patient indexes
CREATE INDEX idx_patient_name ON patients(name);
CREATE INDEX idx_patient_contact ON patients(contact);

-- Doctor indexes
CREATE INDEX idx_doctor_specialization ON doctors(specialization);
CREATE INDEX idx_doctor_email ON doctors(email);

-- Appointment indexes
CREATE INDEX idx_appointment_date ON appointments(appointment_date);
CREATE INDEX idx_appointment_status ON appointments(status);
CREATE INDEX idx_appointment_patient ON appointments(patient_id, appointment_date);
CREATE INDEX idx_appointment_doctor ON appointments(doctor_id, appointment_date);

-- Medical records indexes
CREATE INDEX idx_medical_visit_date ON medical_records(visit_date);
CREATE INDEX idx_medical_patient ON medical_records(patient_id, visit_date);
CREATE INDEX idx_medical_predicted_disease ON medical_records(predicted_disease);

-- User indexes
CREATE INDEX idx_user_role ON users(role);
CREATE INDEX idx_user_active ON users(is_active);

-- Step 5: Verify table creation
SHOW TABLES;

-- Step 6: Display table structures
DESCRIBE patients;
DESCRIBE doctors;
DESCRIBE appointments;
DESCRIBE medical_records;
DESCRIBE users;

-- Success message
SELECT 'Database setup completed successfully!' as Status;