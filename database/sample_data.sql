-- =====================================================
-- Sample Data for Smart Hospital Management System
-- Created by: Krishna + Omkar
-- Date: October 12, 2025
-- Purpose: Test data for Phase 2 development
-- =====================================================

-- Insert Sample Doctors
INSERT INTO doctors (name, specialization, contact, email) VALUES
('Dr. Rajesh Kumar', 'Cardiology', '9876543210', 'rajesh.kumar@hospital.com'),
('Dr. Priya Sharma', 'Pediatrics', '9876543211', 'priya.sharma@hospital.com'),
('Dr. Amit Patel', 'Neurology', '9876543212', 'amit.patel@hospital.com'),
('Dr. Sunita Singh', 'Dermatology', '9876543213', 'sunita.singh@hospital.com'),
('Dr. Vikram Mehta', 'Orthopedics', '9876543214', 'vikram.mehta@hospital.com');

-- Insert Sample Patients
INSERT INTO patients (name, age, gender, contact, address) VALUES
('Ravi Gupta', 45, 'Male', '8765432109', '123 MG Road, Mumbai, Maharashtra'),
('Sneha Joshi', 32, 'Female', '8765432108', '456 Park Street, Delhi, NCR'),
('Arjun Reddy', 28, 'Male', '8765432107', '789 Brigade Road, Bangalore, Karnataka'),
('Kavya Nair', 35, 'Female', '8765432106', '321 Marine Drive, Mumbai, Maharashtra'),
('Rohit Shah', 52, 'Male', '8765432105', '654 Residency Road, Pune, Maharashtra'),
('Anjali Verma', 41, 'Female', '8765432104', '987 Sector 17, Chandigarh, Punjab'),
('Manoj Kumar', 38, 'Male', '8765432103', '147 Civil Lines, Jaipur, Rajasthan'),
('Deepika Rao', 29, 'Female', '8765432102', '258 Koramangala, Bangalore, Karnataka');

-- Insert Sample Appointments
INSERT INTO appointments (patient_id, doctor_id, appointment_date, status, notes) VALUES
(1, 1, '2025-10-15 10:00:00', 'Scheduled', 'Routine cardiac checkup'),
(2, 2, '2025-10-15 11:30:00', 'Scheduled', 'Child vaccination'),
(3, 3, '2025-10-15 14:00:00', 'Completed', 'Headache consultation'),
(4, 4, '2025-10-16 09:15:00', 'Scheduled', 'Skin rash examination'),
(5, 5, '2025-10-16 10:45:00', 'Scheduled', 'Knee pain assessment'),
(6, 1, '2025-10-14 15:30:00', 'Completed', 'Follow-up visit'),
(7, 3, '2025-10-17 12:00:00', 'Scheduled', 'Migraine treatment'),
(8, 2, '2025-10-17 16:30:00', 'Scheduled', 'General health checkup');

-- Insert Sample Medical Records
INSERT INTO medical_records (patient_id, doctor_id, appointment_id, symptoms, diagnosis, predicted_disease, confidence_score, medicines, treatment_notes, visit_date, follow_up_date) VALUES
(3, 3, 3, 'Severe headache, nausea, sensitivity to light', 'Migraine', 'Migraine', 0.92, 'Sumatriptan 50mg, Paracetamol 500mg', 'Patient advised rest and hydration. Avoid triggers.', '2025-10-15 14:00:00', '2025-10-22'),
(6, 1, 6, 'Chest pain, shortness of breath', 'Angina', 'Pneumonia', 0.78, 'Nitroglycerin, Aspirin 75mg', 'ECG normal. Stress test recommended.', '2025-10-14 15:30:00', '2025-10-21');

-- Insert Sample Users (for authentication)
INSERT INTO users (username, password, role, email, is_active) VALUES
('dr_rajesh', 'hashed_password_1', 'Doctor', 'rajesh.kumar@hospital.com', TRUE),
('admin_hospital', 'hashed_password_2', 'Admin', 'admin@hospital.com', TRUE),
('receptionist_1', 'hashed_password_3', 'Receptionist', 'reception@hospital.com', TRUE);

-- =====================================================
-- Verification Queries
-- =====================================================

-- Check all tables have data
SELECT 'Patients' as Table_Name, COUNT(*) as Record_Count FROM patients
UNION ALL
SELECT 'Doctors', COUNT(*) FROM doctors
UNION ALL
SELECT 'Appointments', COUNT(*) FROM appointments
UNION ALL
SELECT 'Medical Records', COUNT(*) FROM medical_records
UNION ALL
SELECT 'Users', COUNT(*) FROM users;

-- View appointments with patient and doctor details
SELECT 
    a.appointment_id,
    p.name as Patient_Name,
    d.name as Doctor_Name,
    d.specialization,
    a.appointment_date,
    a.status
FROM appointments a
JOIN patients p ON a.patient_id = p.patient_id
JOIN doctors d ON a.doctor_id = d.doctor_id
ORDER BY a.appointment_date;

-- View medical records with patient details
SELECT 
    mr.record_id,
    p.name as Patient_Name,
    d.name as Doctor_Name,
    mr.predicted_disease,
    mr.confidence_score,
    mr.visit_date
FROM medical_records mr
JOIN patients p ON mr.patient_id = p.patient_id
JOIN doctors d ON mr.doctor_id = d.doctor_id
ORDER BY mr.visit_date DESC;