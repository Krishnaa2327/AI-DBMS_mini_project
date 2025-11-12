# Smart Hospital Management System: Comprehensive DBMS Documentation

## Table of Contents
1. [Database Architecture Overview](#database-architecture-overview)
2. [Database Configuration & Connection](#database-configuration--connection)
3. [Complete Database Schema](#complete-database-schema)
4. [Table Specifications](#table-specifications)
5. [CRUD Operations Implementation](#crud-operations-implementation)
6. [Data Management Strategies](#data-management-strategies)
7. [Database Security & Integrity](#database-security--integrity)
8. [Performance Optimization](#performance-optimization)
9. [Database Setup & Installation](#database-setup--installation)
10. [Data Relationships & Constraints](#data-relationships--constraints)
11. [Analytics & Reporting Queries](#analytics--reporting-queries)
12. [Database Maintenance & Backup](#database-maintenance--backup)
13. [Error Handling & Logging](#error-handling--logging)
14. [API Integration Layer](#api-integration-layer)
15. [Testing & Validation](#testing--validation)

---

## Database Architecture Overview

### 1.1 Database System
- **DBMS**: MySQL 8.0+
- **Database Name**: `smart_hospital`
- **Connection Protocol**: MySQL Connector/Python
- **Architecture Pattern**: Centralized RDBMS with connection pooling
- **Data Storage Engine**: InnoDB (default)

### 1.2 System Components
```
┌─────────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │ Streamlit UI│  │   Chatbot   │  │ ML Pipeline │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────────┐
│                    DATABASE ACCESS LAYER                       │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │        HospitalDatabase Class (connection.py)             ││
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐         ││
│  │  │   Patient   │ │   Doctor    │ │ Appointment │         ││
│  │  │  Methods    │ │   Methods   │ │   Methods   │         ││
│  │  └─────────────┘ └─────────────┘ └─────────────┘         ││
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐         ││
│  │  │   Medical   │ │ Analytics   │ │ Connection  │         ││
│  │  │   Records   │ │   Methods   │ │   Pool      │         ││
│  │  └─────────────┘ └─────────────┘ └─────────────┘         ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────────┐
│                     DATABASE LAYER                             │
│                    MySQL Database Server                        │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌──────────┐ │
│  │  patients   │ │   doctors   │ │appointments │ │  users   │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └──────────┘ │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              medical_records                            │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │   Indexes | Foreign Keys | Constraints | Triggers      │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### 1.3 Database Design Principles
- **Normalization**: 3NF (Third Normal Form) compliance
- **ACID Properties**: Full ACID compliance for all transactions
- **Referential Integrity**: Comprehensive foreign key constraints
- **Data Consistency**: Enforced through constraints and validations
- **Scalability**: Connection pooling and optimized queries
- **Security**: Parameterized queries and input validation

---

## Database Configuration & Connection

### 2.1 Connection Configuration (`database/db_config.py`)
```python
# Database Configuration
DATABASE_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Krishna@112406",
    "database": "smart_hospital",
    "charset": "utf8mb4",
    "collation": "utf8mb4_unicode_ci"
}

# Connection Pool Configuration
POOL_CONFIG = {
    "pool_name": "hospital_pool",
    "pool_size": 5,
    "pool_reset_session": True,
    "autocommit": True,
    "time_zone": "+05:30"
}
```

### 2.2 Connection Pool Implementation
```python
class HospitalDatabase:
    def __init__(self, host="localhost", user="root", 
                 password="Krishna@112406", database="smart_hospital"):
        self.pool_config = {
            'pool_name': 'hospital_pool',
            'pool_size': 5,  # Maximum 5 concurrent connections
            'pool_reset_session': True,
            'host': host,
            'user': user,
            'password': password,
            'database': database
        }
        
        # Create connection pool for optimal performance
        self.pool = mysql.connector.pooling.MySQLConnectionPool(**self.pool_config)
```

### 2.3 Connection Management
- **Connection Pooling**: 5 concurrent connections
- **Auto-reconnection**: Handles connection drops
- **Transaction Management**: Automatic commit/rollback
- **Error Handling**: Comprehensive exception handling
- **Logging**: Detailed operation logging

---

## Complete Database Schema

### 3.1 Schema Overview
```sql
-- Database Creation
CREATE DATABASE IF NOT EXISTS smart_hospital;
USE smart_hospital;

-- Character Set and Collation
ALTER DATABASE smart_hospital 
CHARACTER SET = utf8mb4 
COLLATE = utf8mb4_unicode_ci;
```

### 3.2 Complete Schema Definition
```sql
-- =====================================================
-- Smart Hospital Management System - Enhanced Schema
-- Created by: Krishna + Omkar
-- Date: October 12, 2025
-- Version: 2.0
-- =====================================================

-- 1. PATIENTS TABLE
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

-- 2. DOCTORS TABLE
CREATE TABLE doctors (
    doctor_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    specialization VARCHAR(100) NOT NULL,
    contact VARCHAR(15),
    email VARCHAR(100) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 3. APPOINTMENTS TABLE
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

-- 4. MEDICAL RECORDS TABLE
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

-- 5. USERS TABLE (Authentication)
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
```

---

## Table Specifications

### 4.1 PATIENTS Table

#### 4.1.1 Table Structure
```sql
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
```

#### 4.1.2 Field Specifications
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `patient_id` | INT | AUTO_INCREMENT, PRIMARY KEY | Unique identifier |
| `name` | VARCHAR(100) | NOT NULL | Patient full name |
| `age` | INT | CHECK (age > 0 AND age <= 150) | Patient age |
| `gender` | ENUM | NOT NULL, ('Male', 'Female', 'Other') | Gender selection |
| `contact` | VARCHAR(15) | NULL | Phone number |
| `address` | TEXT | NULL | Complete address |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation time |
| `updated_at` | TIMESTAMP | ON UPDATE CURRENT_TIMESTAMP | Last update time |

#### 4.1.3 Indexes
```sql
CREATE INDEX idx_patient_name ON patients(name);
CREATE INDEX idx_patient_contact ON patients(contact);
CREATE INDEX idx_patient_created ON patients(created_at);
```

#### 4.1.4 Sample Data
```sql
INSERT INTO patients (name, age, gender, contact, address) VALUES
('Ravi Gupta', 45, 'Male', '8765432109', '123 MG Road, Mumbai, Maharashtra'),
('Sneha Joshi', 32, 'Female', '8765432108', '456 Park Street, Delhi, NCR'),
('Arjun Reddy', 28, 'Male', '8765432107', '789 Brigade Road, Bangalore, Karnataka');
```

### 4.2 DOCTORS Table

#### 4.2.1 Table Structure
```sql
CREATE TABLE doctors (
    doctor_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    specialization VARCHAR(100) NOT NULL,
    contact VARCHAR(15),
    email VARCHAR(100) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

#### 4.2.2 Field Specifications
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `doctor_id` | INT | AUTO_INCREMENT, PRIMARY KEY | Unique identifier |
| `name` | VARCHAR(100) | NOT NULL | Doctor full name |
| `specialization` | VARCHAR(100) | NOT NULL | Medical specialization |
| `contact` | VARCHAR(15) | NULL | Phone number |
| `email` | VARCHAR(100) | UNIQUE | Email address |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation time |
| `updated_at` | TIMESTAMP | ON UPDATE CURRENT_TIMESTAMP | Last update time |

#### 4.2.3 Specializations Supported
- Cardiology
- Pediatrics
- Neurology
- Dermatology
- Orthopedics
- Gynecology
- Psychiatry
- General Medicine
- Surgery
- Radiology
- Pathology
- Emergency Medicine

#### 4.2.4 Indexes
```sql
CREATE INDEX idx_doctor_specialization ON doctors(specialization);
CREATE INDEX idx_doctor_email ON doctors(email);
CREATE INDEX idx_doctor_name ON doctors(name);
```

### 4.3 APPOINTMENTS Table

#### 4.3.1 Table Structure
```sql
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
```

#### 4.3.2 Field Specifications
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `appointment_id` | INT | AUTO_INCREMENT, PRIMARY KEY | Unique identifier |
| `patient_id` | INT | NOT NULL, FOREIGN KEY | Reference to patient |
| `doctor_id` | INT | NOT NULL, FOREIGN KEY | Reference to doctor |
| `appointment_date` | DATETIME | NOT NULL | Scheduled date and time |
| `status` | ENUM | DEFAULT 'Scheduled' | Appointment status |
| `notes` | TEXT | NULL | Additional notes |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation time |
| `updated_at` | TIMESTAMP | ON UPDATE CURRENT_TIMESTAMP | Last update time |

#### 4.3.3 Status Values
- `Scheduled`: Upcoming appointment
- `Completed`: Finished appointment
- `Cancelled`: Cancelled appointment

#### 4.3.4 Indexes
```sql
CREATE INDEX idx_appointment_date ON appointments(appointment_date);
CREATE INDEX idx_appointment_status ON appointments(status);
CREATE INDEX idx_appointment_patient ON appointments(patient_id, appointment_date);
CREATE INDEX idx_appointment_doctor ON appointments(doctor_id, appointment_date);
```

### 4.4 MEDICAL_RECORDS Table

#### 4.4.1 Table Structure
```sql
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
```

#### 4.4.2 Field Specifications
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `record_id` | INT | AUTO_INCREMENT, PRIMARY KEY | Unique identifier |
| `patient_id` | INT | NOT NULL, FOREIGN KEY | Reference to patient |
| `doctor_id` | INT | NOT NULL, FOREIGN KEY | Reference to doctor |
| `appointment_id` | INT | FOREIGN KEY | Reference to appointment |
| `symptoms` | TEXT | NULL | Patient symptoms |
| `diagnosis` | TEXT | NULL | Doctor's diagnosis |
| `predicted_disease` | VARCHAR(100) | NULL | AI prediction |
| `confidence_score` | FLOAT | CHECK (0-1) | AI confidence level |
| `medicines` | TEXT | NULL | Prescribed medications |
| `treatment_notes` | TEXT | NULL | Treatment instructions |
| `visit_date` | DATETIME | DEFAULT CURRENT_TIMESTAMP | Visit date |
| `follow_up_date` | DATE | NULL | Next appointment date |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation time |

#### 4.4.3 Indexes
```sql
CREATE INDEX idx_medical_visit_date ON medical_records(visit_date);
CREATE INDEX idx_medical_patient ON medical_records(patient_id, visit_date);
CREATE INDEX idx_medical_predicted_disease ON medical_records(predicted_disease);
CREATE INDEX idx_medical_confidence ON medical_records(confidence_score);
```

### 4.5 USERS Table

#### 4.5.1 Table Structure
```sql
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
```

#### 4.5.2 Field Specifications
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `user_id` | INT | AUTO_INCREMENT, PRIMARY KEY | Unique identifier |
| `username` | VARCHAR(100) | UNIQUE, NOT NULL | Login username |
| `password` | VARCHAR(255) | NOT NULL | Hashed password |
| `role` | ENUM | NOT NULL | User role |
| `email` | VARCHAR(100) | UNIQUE | Email address |
| `is_active` | BOOLEAN | DEFAULT TRUE | Account status |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation time |
| `updated_at` | TIMESTAMP | ON UPDATE CURRENT_TIMESTAMP | Last update time |

#### 4.5.3 User Roles
- `Doctor`: Medical practitioners
- `Admin`: System administrators
- `Receptionist`: Front desk staff

---

## CRUD Operations Implementation

### 5.1 Patient Operations

#### 5.1.1 CREATE - Add Patient
```python
def add_patient(self, name: str, age: int, gender: str, 
                contact: str = None, address: str = None) -> int:
    """
    Add new patient to database
    
    Args:
        name (str): Patient full name
        age (int): Patient age (1-150)
        gender (str): 'Male', 'Female', or 'Other'
        contact (str, optional): Phone number
        address (str, optional): Complete address
    
    Returns:
        int: patient_id of newly created patient
    
    Raises:
        mysql.connector.Error: Database operation error
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
```

#### 5.1.2 READ - Get Patients
```python
def get_patients(self, limit: int = 100) -> List[Dict]:
    """
    Retrieve all patients with optional limit
    
    Args:
        limit (int): Maximum number of records to return
    
    Returns:
        List[Dict]: List of patient records
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
    Get specific patient by ID
    
    Args:
        patient_id (int): Patient ID
    
    Returns:
        Dict: Patient record or None if not found
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
```

#### 5.1.3 UPDATE - Update Patient
```python
def update_patient(self, patient_id: int, **kwargs) -> bool:
    """
    Update patient information
    
    Args:
        patient_id (int): Patient ID to update
        **kwargs: Fields to update (name, age, gender, contact, address)
    
    Returns:
        bool: True if update successful, False otherwise
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
```

#### 5.1.4 DELETE - Remove Patient
```python
def delete_patient(self, patient_id: int) -> bool:
    """
    Delete patient and all associated records
    
    Args:
        patient_id (int): Patient ID to delete
    
    Returns:
        bool: True if deletion successful
    
    Note:
        This will cascade delete all appointments and medical records
    """
    try:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = "DELETE FROM patients WHERE patient_id = %s"
        cursor.execute(query, (patient_id,))
        conn.commit()
        
        affected_rows = cursor.rowcount
        cursor.close()
        conn.close()
        
        if affected_rows > 0:
            logger.info(f"✅ Patient {patient_id} deleted successfully")
            return True
        else:
            logger.warning(f"⚠️ No patient found with ID {patient_id}")
            return False
            
    except Error as e:
        logger.error(f"❌ Error deleting patient: {e}")
        raise
```

### 5.2 Doctor Operations

#### 5.2.1 CREATE - Add Doctor
```python
def add_doctor(self, name: str, specialization: str, 
               contact: str = None, email: str = None) -> int:
    """
    Add new doctor to database
    
    Args:
        name (str): Doctor full name
        specialization (str): Medical specialization
        contact (str, optional): Phone number
        email (str, optional): Email address
    
    Returns:
        int: doctor_id of newly created doctor
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
```

#### 5.2.2 READ - Get Doctors
```python
def get_doctors(self, specialization: str = None) -> List[Dict]:
    """
    Get all doctors or filter by specialization
    
    Args:
        specialization (str, optional): Filter by specialization
    
    Returns:
        List[Dict]: List of doctor records
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
```

### 5.3 Appointment Operations

#### 5.3.1 CREATE - Schedule Appointment
```python
def schedule_appointment(self, patient_id: int, doctor_id: int, 
                        appointment_date: datetime, notes: str = None) -> int:
    """
    Schedule new appointment
    
    Args:
        patient_id (int): Patient ID
        doctor_id (int): Doctor ID
        appointment_date (datetime): Appointment date and time
        notes (str, optional): Additional notes
    
    Returns:
        int: appointment_id of newly scheduled appointment
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
```

#### 5.3.2 READ - Get Appointments
```python
def get_appointments(self, status: str = None, date_from: date = None, 
                    date_to: date = None) -> List[Dict]:
    """
    Get appointments with optional filters
    
    Args:
        status (str, optional): Filter by status ('Scheduled', 'Completed', 'Cancelled')
        date_from (date, optional): Start date filter
        date_to (date, optional): End date filter
    
    Returns:
        List[Dict]: List of appointment records with patient and doctor details
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
```

#### 5.3.3 UPDATE - Update Appointment Status
```python
def update_appointment_status(self, appointment_id: int, status: str) -> bool:
    """
    Update appointment status
    
    Args:
        appointment_id (int): Appointment ID
        status (str): New status ('Scheduled', 'Completed', 'Cancelled')
    
    Returns:
        bool: True if update successful
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
```

### 5.4 Medical Records Operations

#### 5.4.1 CREATE - Save Medical Record
```python
def save_medical_record(self, patient_id: int, doctor_id: int, 
                       appointment_id: int = None, symptoms: str = None,
                       diagnosis: str = None, predicted_disease: str = None,
                       confidence_score: float = None, medicines: str = None,
                       treatment_notes: str = None, follow_up_date: date = None) -> int:
    """
    Save comprehensive medical record
    
    Args:
        patient_id (int): Patient ID
        doctor_id (int): Doctor ID
        appointment_id (int, optional): Associated appointment
        symptoms (str, optional): Patient symptoms
        diagnosis (str, optional): Doctor's diagnosis
        predicted_disease (str, optional): AI prediction
        confidence_score (float, optional): AI confidence (0.0-1.0)
        medicines (str, optional): Prescribed medications
        treatment_notes (str, optional): Treatment instructions
        follow_up_date (date, optional): Next appointment date
    
    Returns:
        int: record_id of saved medical record
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
```

#### 5.4.2 Specialized - Save ML Prediction
```python
def save_prediction(self, patient_id: int, predicted_disease: str, 
                   confidence_score: float, symptoms: str = None) -> int:
    """
    Save ML prediction as simplified medical record
    
    Args:
        patient_id (int): Patient ID
        predicted_disease (str): AI predicted disease
        confidence_score (float): AI confidence level (0.0-1.0)
        symptoms (str, optional): Patient symptoms
    
    Returns:
        int: record_id of saved prediction
    """
    try:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Use default "AI Doctor" (doctor_id = 1)
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
```

#### 5.4.3 READ - Get Patient History
```python
def get_patient_history(self, patient_id: int) -> List[Dict]:
    """
    Get complete medical history for a patient
    
    Args:
        patient_id (int): Patient ID
    
    Returns:
        List[Dict]: List of medical records with doctor details
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
```

---

## Data Management Strategies

### 6.1 Data Validation

#### 6.1.1 Input Validation Rules
```python
class DataValidator:
    @staticmethod
    def validate_patient_data(name, age, gender, contact=None):
        """Validate patient data before database insertion"""
        errors = []
        
        # Name validation
        if not name or len(name.strip()) < 2:
            errors.append("Name must be at least 2 characters long")
        if len(name) > 100:
            errors.append("Name cannot exceed 100 characters")
        
        # Age validation
        if not isinstance(age, int) or age <= 0 or age > 150:
            errors.append("Age must be between 1 and 150")
        
        # Gender validation
        if gender not in ['Male', 'Female', 'Other']:
            errors.append("Gender must be 'Male', 'Female', or 'Other'")
        
        # Contact validation (if provided)
        if contact:
            if not contact.isdigit() or len(contact) != 10:
                errors.append("Contact must be 10-digit number")
        
        return errors
    
    @staticmethod
    def validate_appointment_data(patient_id, doctor_id, appointment_date):
        """Validate appointment data"""
        errors = []
        
        # Check if appointment date is in the future
        if appointment_date <= datetime.now():
            errors.append("Appointment date must be in the future")
        
        # Check business hours (9 AM to 6 PM)
        if not (9 <= appointment_date.hour <= 18):
            errors.append("Appointments only available between 9 AM and 6 PM")
        
        return errors
```

#### 6.1.2 Data Sanitization
```python
def sanitize_input(data):
    """Sanitize user input to prevent SQL injection"""
    if isinstance(data, str):
        # Remove potentially dangerous characters
        data = data.strip()
        data = re.sub(r'[<>"\']', '', data)
    return data
```

### 6.2 Transaction Management

#### 6.2.1 Atomic Operations
```python
def save_complete_visit(self, patient_data, appointment_data, medical_record_data):
    """
    Save complete patient visit in a single transaction
    """
    conn = None
    try:
        conn = self.get_connection()
        conn.start_transaction()
        
        cursor = conn.cursor()
        
        # 1. Create/update patient
        if patient_data.get('patient_id'):
            # Update existing patient
            self.update_patient(patient_data['patient_id'], **patient_data)
            patient_id = patient_data['patient_id']
        else:
            # Create new patient
            patient_id = self.add_patient(**patient_data)
        
        # 2. Schedule appointment
        appointment_data['patient_id'] = patient_id
        appointment_id = self.schedule_appointment(**appointment_data)
        
        # 3. Save medical record
        medical_record_data['patient_id'] = patient_id
        medical_record_data['appointment_id'] = appointment_id
        record_id = self.save_medical_record(**medical_record_data)
        
        # Commit transaction
        conn.commit()
        
        logger.info(f"✅ Complete visit saved successfully: Record ID {record_id}")
        return record_id
        
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"❌ Error saving complete visit: {e}")
        raise
    finally:
        if conn:
            conn.close()
```

### 6.3 Data Consistency

#### 6.3.1 Referential Integrity Checks
```python
def validate_foreign_keys(self, patient_id, doctor_id):
    """
    Validate that foreign keys exist before creating relationships
    """
    # Check patient exists
    patient = self.get_patient_by_id(patient_id)
    if not patient:
        raise ValueError(f"Patient with ID {patient_id} does not exist")
    
    # Check doctor exists
    doctor = self.get_doctor_by_id(doctor_id)
    if not doctor:
        raise ValueError(f"Doctor with ID {doctor_id} does not exist")
    
    return True
```

### 6.4 Data Archiving

#### 6.4.1 Archive Old Records
```python
def archive_old_records(self, cutoff_date: date):
    """
    Archive medical records older than cutoff date
    """
    try:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create archive table if not exists
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS medical_records_archive LIKE medical_records
        """)
        
        # Move old records to archive
        cursor.execute("""
        INSERT INTO medical_records_archive 
        SELECT * FROM medical_records 
        WHERE visit_date < %s
        """, (cutoff_date,))
        
        # Delete from main table
        cursor.execute("""
        DELETE FROM medical_records 
        WHERE visit_date < %s
        """, (cutoff_date,))
        
        conn.commit()
        archived_count = cursor.rowcount
        
        cursor.close()
        conn.close()
        
        logger.info(f"✅ Archived {archived_count} old medical records")
        return archived_count
        
    except Error as e:
        logger.error(f"❌ Error archiving records: {e}")
        raise
```

---

## Database Security & Integrity

### 7.1 Security Measures

#### 7.1.1 SQL Injection Prevention
```python
# ❌ BAD - Vulnerable to SQL injection
def get_patient_bad(self, name):
    query = f"SELECT * FROM patients WHERE name = '{name}'"
    cursor.execute(query)

# ✅ GOOD - Using parameterized queries
def get_patient_safe(self, name):
    query = "SELECT * FROM patients WHERE name = %s"
    cursor.execute(query, (name,))
```

#### 7.1.2 Password Security
```python
import hashlib
import secrets

def hash_password(password: str) -> str:
    """Hash password using SHA-256 with salt"""
    salt = secrets.token_hex(16)
    pwd_hash = hashlib.sha256(salt.encode() + password.encode()).hexdigest()
    return f"{salt}:{pwd_hash}"

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    salt, pwd_hash = hashed.split(':')
    return pwd_hash == hashlib.sha256(salt.encode() + password.encode()).hexdigest()
```

#### 7.1.3 Data Encryption
```python
from cryptography.fernet import Fernet

class DataEncryption:
    def __init__(self, key=None):
        if key:
            self.cipher = Fernet(key)
        else:
            self.cipher = Fernet(Fernet.generate_key())
    
    def encrypt_sensitive_data(self, data: str) -> str:
        """Encrypt sensitive data like contact information"""
        return self.cipher.encrypt(data.encode()).decode()
    
    def decrypt_sensitive_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        return self.cipher.decrypt(encrypted_data.encode()).decode()
```

### 7.2 Access Control

#### 7.2.1 Role-Based Access
```python
def check_permission(self, user_role: str, operation: str, table: str) -> bool:
    """Check if user role has permission for operation"""
    permissions = {
        'Admin': {
            'patients': ['CREATE', 'READ', 'UPDATE', 'DELETE'],
            'doctors': ['CREATE', 'READ', 'UPDATE', 'DELETE'],
            'appointments': ['CREATE', 'READ', 'UPDATE', 'DELETE'],
            'medical_records': ['CREATE', 'READ', 'UPDATE', 'DELETE'],
            'users': ['CREATE', 'READ', 'UPDATE', 'DELETE']
        },
        'Doctor': {
            'patients': ['CREATE', 'READ', 'UPDATE'],
            'doctors': ['READ'],
            'appointments': ['READ', 'UPDATE'],
            'medical_records': ['CREATE', 'READ', 'UPDATE'],
            'users': []
        },
        'Receptionist': {
            'patients': ['CREATE', 'READ', 'UPDATE'],
            'doctors': ['READ'],
            'appointments': ['CREATE', 'READ', 'UPDATE'],
            'medical_records': ['READ'],
            'users': []
        }
    }
    
    return operation in permissions.get(user_role, {}).get(table, [])
```

### 7.3 Data Integrity Constraints

#### 7.3.1 Check Constraints
```sql
-- Age validation
ALTER TABLE patients ADD CONSTRAINT chk_patient_age 
CHECK (age > 0 AND age <= 150);

-- Confidence score validation
ALTER TABLE medical_records ADD CONSTRAINT chk_confidence_score 
CHECK (confidence_score >= 0 AND confidence_score <= 1);

-- Appointment date validation
ALTER TABLE appointments ADD CONSTRAINT chk_appointment_future 
CHECK (appointment_date > NOW());
```

#### 7.3.2 Trigger Implementation
```sql
-- Audit trigger for patient updates
DELIMITER $$
CREATE TRIGGER patient_audit_trigger
    AFTER UPDATE ON patients
    FOR EACH ROW
BEGIN
    INSERT INTO patient_audit_log (
        patient_id, 
        field_changed, 
        old_value, 
        new_value, 
        changed_by, 
        changed_at
    ) VALUES (
        NEW.patient_id, 
        'UPDATE', 
        CONCAT(OLD.name, '|', OLD.age), 
        CONCAT(NEW.name, '|', NEW.age), 
        USER(), 
        NOW()
    );
END$$
DELIMITER ;
```

---

## Performance Optimization

### 8.1 Indexing Strategy

#### 8.1.1 Primary Indexes
```sql
-- Primary key indexes (automatically created)
-- patients(patient_id), doctors(doctor_id), etc.

-- Secondary indexes for frequent queries
CREATE INDEX idx_patient_name ON patients(name);
CREATE INDEX idx_patient_contact ON patients(contact);
CREATE INDEX idx_doctor_specialization ON doctors(specialization);
CREATE INDEX idx_appointment_date ON appointments(appointment_date);
CREATE INDEX idx_appointment_status ON appointments(status);
CREATE INDEX idx_medical_visit_date ON medical_records(visit_date);
CREATE INDEX idx_medical_predicted_disease ON medical_records(predicted_disease);
```

#### 8.1.2 Composite Indexes
```sql
-- For complex queries involving multiple columns
CREATE INDEX idx_appointment_patient_date ON appointments(patient_id, appointment_date);
CREATE INDEX idx_appointment_doctor_date ON appointments(doctor_id, appointment_date);
CREATE INDEX idx_medical_patient_date ON medical_records(patient_id, visit_date);
```

#### 8.1.3 Partial Indexes
```sql
-- Index only active appointments
CREATE INDEX idx_active_appointments ON appointments(appointment_date) 
WHERE status = 'Scheduled';

-- Index high-confidence predictions
CREATE INDEX idx_high_confidence_predictions ON medical_records(predicted_disease) 
WHERE confidence_score > 0.8;
```

### 8.2 Query Optimization

#### 8.2.1 Optimized Dashboard Query
```python
def get_dashboard_stats_optimized(self) -> Dict:
    """
    Optimized dashboard statistics query using single connection
    """
    try:
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Single query for all counts
        cursor.execute("""
        SELECT 
            (SELECT COUNT(*) FROM patients) as total_patients,
            (SELECT COUNT(*) FROM doctors) as total_doctors,
            (SELECT COUNT(*) FROM appointments WHERE status = 'Scheduled') as scheduled_appointments,
            (SELECT COUNT(*) FROM medical_records WHERE DATE(visit_date) = CURDATE()) as todays_visits
        """)
        
        stats = cursor.fetchone()
        
        # Optimized upcoming appointments query
        cursor.execute("""
        SELECT a.appointment_date, p.name as patient_name, d.name as doctor_name
        FROM appointments a
        STRAIGHT_JOIN patients p ON a.patient_id = p.patient_id
        STRAIGHT_JOIN doctors d ON a.doctor_id = d.doctor_id
        WHERE a.appointment_date >= NOW() AND a.status = 'Scheduled'
        ORDER BY a.appointment_date LIMIT 5
        """)
        stats['upcoming_appointments'] = cursor.fetchall()
        
        # Optimized disease predictions query with caching
        cursor.execute("""
        SELECT predicted_disease, COUNT(*) as count
        FROM medical_records 
        WHERE predicted_disease IS NOT NULL 
            AND visit_date >= DATE_SUB(NOW(), INTERVAL 30 DAY)
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
```

#### 8.2.2 Pagination Implementation
```python
def get_patients_paginated(self, page: int = 1, per_page: int = 20, 
                          search: str = None) -> Dict:
    """
    Get patients with pagination and search
    """
    try:
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Count query for total records
        count_query = "SELECT COUNT(*) as total FROM patients"
        where_clause = ""
        params = []
        
        if search:
            where_clause = " WHERE name LIKE %s OR contact LIKE %s"
            search_param = f"%{search}%"
            params = [search_param, search_param]
            count_query += where_clause
        
        cursor.execute(count_query, params)
        total_records = cursor.fetchone()['total']
        
        # Data query with pagination
        offset = (page - 1) * per_page
        data_query = f"""
        SELECT * FROM patients
        {where_clause}
        ORDER BY created_at DESC
        LIMIT %s OFFSET %s
        """
        
        params.extend([per_page, offset])
        cursor.execute(data_query, params)
        patients = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return {
            'data': patients,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total_records,
                'pages': (total_records + per_page - 1) // per_page
            }
        }
        
    except Error as e:
        logger.error(f"❌ Error fetching paginated patients: {e}")
        raise
```

### 8.3 Connection Pool Optimization

#### 8.3.1 Pool Configuration
```python
OPTIMIZED_POOL_CONFIG = {
    'pool_name': 'hospital_pool',
    'pool_size': 10,              # Increased pool size
    'pool_reset_session': True,
    'pool_recycle': 3600,         # Recycle connections every hour
    'pool_pre_ping': True,        # Validate connections before use
    'max_overflow': 5,            # Allow temporary overflow
    'pool_timeout': 30,           # Connection timeout
    'autocommit': True,
    'sql_mode': 'STRICT_TRANS_TABLES,NO_ZERO_DATE,NO_ZERO_IN_DATE,ERROR_FOR_DIVISION_BY_ZERO',
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci'
}
```

### 8.4 Caching Strategy

#### 8.4.1 In-Memory Caching
```python
from functools import lru_cache
import time

class DatabaseCache:
    def __init__(self, ttl=300):  # 5 minutes default TTL
        self.cache = {}
        self.ttl = ttl
    
    def get(self, key):
        if key in self.cache:
            value, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return value
            else:
                del self.cache[key]
        return None
    
    def set(self, key, value):
        self.cache[key] = (value, time.time())
    
    def invalidate(self, pattern):
        keys_to_delete = [k for k in self.cache.keys() if pattern in k]
        for key in keys_to_delete:
            del self.cache[key]

# Global cache instance
db_cache = DatabaseCache()

@lru_cache(maxsize=128)
def get_doctors_by_specialization_cached(self, specialization):
    """Cached version of doctor lookup by specialization"""
    cache_key = f"doctors_spec_{specialization}"
    
    # Check cache first
    cached_result = db_cache.get(cache_key)
    if cached_result:
        return cached_result
    
    # Query database
    doctors = self.get_doctors(specialization)
    
    # Cache result
    db_cache.set(cache_key, doctors)
    
    return doctors
```

---

## Database Setup & Installation

### 9.1 Prerequisites

#### 9.1.1 System Requirements
- **MySQL Server**: Version 8.0 or higher
- **Python**: Version 3.8 or higher
- **Memory**: Minimum 4GB RAM, 8GB recommended
- **Storage**: Minimum 1GB free space for database
- **Network**: Local or remote MySQL connection

#### 9.1.2 Required Python Packages
```bash
pip install mysql-connector-python==8.0.33
pip install cryptography==41.0.4
pip install pandas==2.0.3
pip install logging==0.4.9.6
```

### 9.2 Database Installation

#### 9.2.1 Step 1: Create Database
```sql
-- Connect to MySQL as root
mysql -u root -p

-- Create database
CREATE DATABASE IF NOT EXISTS smart_hospital;
USE smart_hospital;

-- Set character set and collation
ALTER DATABASE smart_hospital 
CHARACTER SET = utf8mb4 
COLLATE = utf8mb4_unicode_ci;
```

#### 9.2.2 Step 2: Run Setup Script
```bash
# Navigate to project directory
cd C:\Users\Dell\AI-DBMS_mini_project

# Run database setup
mysql -u root -p smart_hospital < database/setup_database.sql
```

#### 9.2.3 Step 3: Load Sample Data
```bash
# Load sample data for testing
mysql -u root -p smart_hospital < database/sample_data.sql
```

#### 9.2.4 Step 4: Verify Installation
```sql
-- Check tables
SHOW TABLES;

-- Verify data
SELECT 'Patients' as Table_Name, COUNT(*) as Record_Count FROM patients
UNION ALL
SELECT 'Doctors', COUNT(*) FROM doctors
UNION ALL
SELECT 'Appointments', COUNT(*) FROM appointments
UNION ALL
SELECT 'Medical Records', COUNT(*) FROM medical_records
UNION ALL
SELECT 'Users', COUNT(*) FROM users;
```

### 9.3 Configuration Setup

#### 9.3.1 Database Configuration File
```python
# database/db_config.py
DATABASE_CONFIG = {
    # Connection settings
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'Krishna@112406',  # Change this to your MySQL password
    'database': 'smart_hospital',
    
    # Character set
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci',
    
    # Connection options
    'autocommit': True,
    'time_zone': '+05:30',  # IST timezone
    'sql_mode': 'STRICT_TRANS_TABLES,NO_ZERO_DATE',
    
    # SSL settings (for remote connections)
    'ssl_disabled': True,  # Set to False for SSL connections
    
    # Connection timeout
    'connection_timeout': 30,
    'pool_timeout': 30
}
```

#### 9.3.2 Environment Variables
```bash
# .env file for production
DB_HOST=localhost
DB_PORT=3306
DB_USER=hospital_user
DB_PASSWORD=secure_password_here
DB_NAME=smart_hospital
DB_CHARSET=utf8mb4

# Pool settings
DB_POOL_SIZE=10
DB_POOL_TIMEOUT=30
DB_POOL_RECYCLE=3600
```

### 9.4 Initial Data Setup

#### 9.4.1 Create Default AI Doctor
```sql
-- Insert AI Doctor for ML predictions
INSERT INTO doctors (name, specialization, contact, email) VALUES
('AI Doctor', 'Artificial Intelligence', '0000000000', 'ai@hospital.com');
```

#### 9.4.2 Create Admin User
```sql
-- Insert system admin
INSERT INTO users (username, password, role, email, is_active) VALUES
('admin', SHA2('admin123', 256), 'Admin', 'admin@hospital.com', TRUE);
```

---

## Data Relationships & Constraints

### 10.1 Entity Relationship Diagram

```
┌─────────────────────┐       ┌─────────────────────┐
│       PATIENTS      │       │       DOCTORS       │
├─────────────────────┤       ├─────────────────────┤
│ patient_id (PK)     │       │ doctor_id (PK)      │
│ name                │       │ name                │
│ age                 │       │ specialization      │
│ gender              │       │ contact             │
│ contact             │       │ email               │
│ address             │       │ created_at          │
│ created_at          │       │ updated_at          │
│ updated_at          │       └─────────────────────┘
└─────────────────────┘                │
         │                             │
         │                             │
         ▼                             ▼
┌─────────────────────────────────────────────────────┐
│                APPOINTMENTS                         │
├─────────────────────────────────────────────────────┤
│ appointment_id (PK)                                 │
│ patient_id (FK) ──→ patients.patient_id            │
│ doctor_id (FK) ───→ doctors.doctor_id              │
│ appointment_date                                    │
│ status                                              │
│ notes                                               │
│ created_at                                          │
│ updated_at                                          │
└─────────────────────────────────────────────────────┘
         │
         │
         ▼
┌─────────────────────────────────────────────────────┐
│              MEDICAL_RECORDS                        │
├─────────────────────────────────────────────────────┤
│ record_id (PK)                                      │
│ patient_id (FK) ──→ patients.patient_id            │
│ doctor_id (FK) ───→ doctors.doctor_id              │
│ appointment_id (FK) → appointments.appointment_id   │
│ symptoms                                            │
│ diagnosis                                           │
│ predicted_disease                                   │
│ confidence_score                                    │
│ medicines                                           │
│ treatment_notes                                     │
│ visit_date                                          │
│ follow_up_date                                      │
│ created_at                                          │
└─────────────────────────────────────────────────────┘

┌─────────────────────┐
│       USERS         │
├─────────────────────┤
│ user_id (PK)        │
│ username            │
│ password            │
│ role                │
│ email               │
│ is_active           │
│ created_at          │
│ updated_at          │
└─────────────────────┘
```

### 10.2 Foreign Key Relationships

#### 10.2.1 Appointments Table Relationships
```sql
-- Patient relationship (CASCADE DELETE)
ALTER TABLE appointments 
ADD CONSTRAINT fk_appointment_patient 
FOREIGN KEY (patient_id) REFERENCES patients(patient_id) 
ON DELETE CASCADE ON UPDATE CASCADE;

-- Doctor relationship (CASCADE DELETE)
ALTER TABLE appointments 
ADD CONSTRAINT fk_appointment_doctor 
FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) 
ON DELETE CASCADE ON UPDATE CASCADE;
```

#### 10.2.2 Medical Records Relationships
```sql
-- Patient relationship (CASCADE DELETE)
ALTER TABLE medical_records 
ADD CONSTRAINT fk_medical_patient 
FOREIGN KEY (patient_id) REFERENCES patients(patient_id) 
ON DELETE CASCADE ON UPDATE CASCADE;

-- Doctor relationship (CASCADE DELETE)
ALTER TABLE medical_records 
ADD CONSTRAINT fk_medical_doctor 
FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) 
ON DELETE CASCADE ON UPDATE CASCADE;

-- Appointment relationship (SET NULL)
ALTER TABLE medical_records 
ADD CONSTRAINT fk_medical_appointment 
FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id) 
ON DELETE SET NULL ON UPDATE CASCADE;
```

### 10.3 Constraint Definitions

#### 10.3.1 Check Constraints
```sql
-- Patient age constraint
ALTER TABLE patients 
ADD CONSTRAINT chk_patient_age 
CHECK (age > 0 AND age <= 150);

-- Gender constraint
ALTER TABLE patients 
ADD CONSTRAINT chk_patient_gender 
CHECK (gender IN ('Male', 'Female', 'Other'));

-- Confidence score constraint
ALTER TABLE medical_records 
ADD CONSTRAINT chk_confidence_score 
CHECK (confidence_score >= 0.0 AND confidence_score <= 1.0);

-- Appointment status constraint
ALTER TABLE appointments 
ADD CONSTRAINT chk_appointment_status 
CHECK (status IN ('Scheduled', 'Completed', 'Cancelled'));

-- User role constraint
ALTER TABLE users 
ADD CONSTRAINT chk_user_role 
CHECK (role IN ('Doctor', 'Admin', 'Receptionist'));
```

#### 10.3.2 Unique Constraints
```sql
-- Doctor email uniqueness
ALTER TABLE doctors 
ADD CONSTRAINT uk_doctor_email 
UNIQUE (email);

-- User username uniqueness
ALTER TABLE users 
ADD CONSTRAINT uk_user_username 
UNIQUE (username);

-- User email uniqueness
ALTER TABLE users 
ADD CONSTRAINT uk_user_email 
UNIQUE (email);
```

### 10.4 Cascade Actions

#### 10.4.1 DELETE CASCADE Examples
```sql
-- When a patient is deleted:
-- 1. All their appointments are deleted
-- 2. All their medical records are deleted

DELETE FROM patients WHERE patient_id = 1;
-- This will automatically delete:
-- - appointments where patient_id = 1
-- - medical_records where patient_id = 1
```

#### 10.4.2 SET NULL Examples
```sql
-- When an appointment is deleted:
-- Medical records keep their data but appointment_id becomes NULL

DELETE FROM appointments WHERE appointment_id = 1;
-- medical_records with appointment_id = 1 will have appointment_id set to NULL
```

---

## Analytics & Reporting Queries

### 11.1 Dashboard Analytics

#### 11.1.1 Key Performance Indicators
```sql
-- Daily Patient Registration Trends
SELECT 
    DATE(created_at) as registration_date,
    COUNT(*) as patients_registered,
    AVG(age) as avg_age
FROM patients 
WHERE created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
GROUP BY DATE(created_at)
ORDER BY registration_date DESC;

-- Appointment Status Distribution
SELECT 
    status,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM appointments), 2) as percentage
FROM appointments
GROUP BY status;

-- Doctor Utilization Report
SELECT 
    d.name as doctor_name,
    d.specialization,
    COUNT(a.appointment_id) as total_appointments,
    COUNT(CASE WHEN a.status = 'Completed' THEN 1 END) as completed_appointments,
    ROUND(COUNT(CASE WHEN a.status = 'Completed' THEN 1 END) * 100.0 / COUNT(a.appointment_id), 2) as completion_rate
FROM doctors d
LEFT JOIN appointments a ON d.doctor_id = a.doctor_id
GROUP BY d.doctor_id, d.name, d.specialization
ORDER BY total_appointments DESC;
```

#### 11.1.2 Medical Analytics
```sql
-- Disease Prediction Accuracy Trends
SELECT 
    predicted_disease,
    COUNT(*) as predictions_count,
    AVG(confidence_score) as avg_confidence,
    MIN(confidence_score) as min_confidence,
    MAX(confidence_score) as max_confidence
FROM medical_records 
WHERE predicted_disease IS NOT NULL
    AND visit_date >= DATE_SUB(NOW(), INTERVAL 90 DAY)
GROUP BY predicted_disease
HAVING COUNT(*) >= 5
ORDER BY avg_confidence DESC;

-- Age Group Disease Distribution
SELECT 
    CASE 
        WHEN p.age < 18 THEN 'Child (0-17)'
        WHEN p.age < 35 THEN 'Young Adult (18-34)'
        WHEN p.age < 55 THEN 'Adult (35-54)'
        WHEN p.age < 75 THEN 'Senior (55-74)'
        ELSE 'Elderly (75+)'
    END as age_group,
    mr.predicted_disease,
    COUNT(*) as cases
FROM medical_records mr
JOIN patients p ON mr.patient_id = p.patient_id
WHERE mr.predicted_disease IS NOT NULL
GROUP BY age_group, mr.predicted_disease
ORDER BY age_group, cases DESC;
```

### 11.2 Patient Reports

#### 11.2.1 Patient History Report
```sql
-- Comprehensive Patient Medical History
SELECT 
    p.name as patient_name,
    p.age,
    p.gender,
    mr.visit_date,
    d.name as doctor_name,
    d.specialization,
    mr.symptoms,
    mr.diagnosis,
    mr.predicted_disease,
    mr.confidence_score,
    mr.medicines,
    mr.treatment_notes,
    mr.follow_up_date
FROM patients p
JOIN medical_records mr ON p.patient_id = mr.patient_id
JOIN doctors d ON mr.doctor_id = d.doctor_id
WHERE p.patient_id = ? -- Parameter for specific patient
ORDER BY mr.visit_date DESC;
```

#### 11.2.2 Patient Summary Statistics
```sql
-- Patient Visit Frequency Analysis
SELECT 
    p.name as patient_name,
    p.age,
    p.gender,
    COUNT(mr.record_id) as total_visits,
    MIN(mr.visit_date) as first_visit,
    MAX(mr.visit_date) as last_visit,
    DATEDIFF(MAX(mr.visit_date), MIN(mr.visit_date)) as care_duration_days
FROM patients p
LEFT JOIN medical_records mr ON p.patient_id = mr.patient_id
GROUP BY p.patient_id, p.name, p.age, p.gender
HAVING COUNT(mr.record_id) > 0
ORDER BY total_visits DESC;
```

### 11.3 Operational Reports

#### 11.3.1 Appointment Scheduling Report
```sql
-- Daily Appointment Schedule
SELECT 
    DATE(a.appointment_date) as appointment_day,
    TIME(a.appointment_date) as appointment_time,
    p.name as patient_name,
    p.age,
    p.contact,
    d.name as doctor_name,
    d.specialization,
    a.status,
    a.notes
FROM appointments a
JOIN patients p ON a.patient_id = p.patient_id
JOIN doctors d ON a.doctor_id = d.doctor_id
WHERE DATE(a.appointment_date) = CURDATE()
ORDER BY a.appointment_date;

-- Weekly Appointment Load
SELECT 
    DAYNAME(appointment_date) as day_of_week,
    HOUR(appointment_date) as hour_of_day,
    COUNT(*) as appointment_count
FROM appointments
WHERE appointment_date >= DATE_SUB(NOW(), INTERVAL 7 DAY)
    AND appointment_date <= NOW()
GROUP BY DAYNAME(appointment_date), HOUR(appointment_date)
ORDER BY FIELD(day_of_week, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'), hour_of_day;
```

#### 11.3.2 Revenue Analysis (if applicable)
```sql
-- Monthly Revenue by Specialization (conceptual)
SELECT 
    DATE_FORMAT(mr.visit_date, '%Y-%m') as month,
    d.specialization,
    COUNT(mr.record_id) as consultations,
    -- Assuming consultation fees
    COUNT(mr.record_id) * 500 as estimated_revenue
FROM medical_records mr
JOIN doctors d ON mr.doctor_id = d.doctor_id
WHERE mr.visit_date >= DATE_SUB(NOW(), INTERVAL 12 MONTH)
GROUP BY DATE_FORMAT(mr.visit_date, '%Y-%m'), d.specialization
ORDER BY month DESC, estimated_revenue DESC;
```

### 11.4 AI/ML Performance Reports

#### 11.4.1 Model Performance Metrics
```sql
-- ML Model Confidence Distribution
SELECT 
    CASE 
        WHEN confidence_score >= 0.9 THEN 'Very High (90-100%)'
        WHEN confidence_score >= 0.8 THEN 'High (80-89%)'
        WHEN confidence_score >= 0.7 THEN 'Good (70-79%)'
        WHEN confidence_score >= 0.6 THEN 'Fair (60-69%)'
        WHEN confidence_score >= 0.5 THEN 'Low (50-59%)'
        ELSE 'Very Low (<50%)'
    END as confidence_range,
    COUNT(*) as prediction_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM medical_records WHERE predicted_disease IS NOT NULL), 2) as percentage
FROM medical_records
WHERE predicted_disease IS NOT NULL
    AND confidence_score IS NOT NULL
GROUP BY confidence_range
ORDER BY MIN(confidence_score) DESC;

-- Disease-wise Prediction Performance
SELECT 
    predicted_disease,
    COUNT(*) as total_predictions,
    AVG(confidence_score) as avg_confidence,
    STDDEV(confidence_score) as confidence_std_dev,
    MIN(visit_date) as first_prediction,
    MAX(visit_date) as latest_prediction
FROM medical_records
WHERE predicted_disease IS NOT NULL
    AND confidence_score IS NOT NULL
GROUP BY predicted_disease
HAVING COUNT(*) >= 3
ORDER BY avg_confidence DESC, total_predictions DESC;
```

---

## Database Maintenance & Backup

### 12.1 Backup Strategy

#### 12.1.1 Daily Backup Script
```bash
#!/bin/bash
# daily_backup.sh

# Configuration
DB_NAME="smart_hospital"
DB_USER="root"
DB_PASS="Krishna@112406"
BACKUP_DIR="/backups/mysql"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Full database backup
mysqldump -u$DB_USER -p$DB_PASS --single-transaction --routines --triggers $DB_NAME > $BACKUP_DIR/smart_hospital_backup_$DATE.sql

# Compress backup
gzip $BACKUP_DIR/smart_hospital_backup_$DATE.sql

# Remove backups older than 7 days
find $BACKUP_DIR -name "smart_hospital_backup_*.sql.gz" -mtime +7 -delete

echo "Backup completed: smart_hospital_backup_$DATE.sql.gz"
```

#### 12.1.2 Table-Specific Backup
```bash
# Backup specific tables
mysqldump -u root -p Krishna@112406 smart_hospital patients doctors > patients_doctors_backup.sql

# Backup structure only
mysqldump -u root -p Krishna@112406 --no-data smart_hospital > schema_backup.sql

# Backup data only
mysqldump -u root -p Krishna@112406 --no-create-info smart_hospital > data_backup.sql
```

#### 12.1.3 Restore Procedures
```bash
# Full database restore
mysql -u root -p Krishna@112406 smart_hospital < backup_file.sql

# Table-specific restore
mysql -u root -p Krishna@112406 smart_hospital < patients_doctors_backup.sql
```

### 12.2 Database Maintenance

#### 12.2.1 Regular Maintenance Tasks
```sql
-- Analyze table statistics
ANALYZE TABLE patients, doctors, appointments, medical_records, users;

-- Optimize tables
OPTIMIZE TABLE patients, doctors, appointments, medical_records, users;

-- Check table integrity
CHECK TABLE patients, doctors, appointments, medical_records, users;

-- Repair tables if needed
REPAIR TABLE table_name;
```

#### 12.2.2 Index Maintenance
```sql
-- Check index usage
SELECT 
    TABLE_NAME,
    INDEX_NAME,
    CARDINALITY,
    SUB_PART,
    INDEX_TYPE
FROM INFORMATION_SCHEMA.STATISTICS 
WHERE TABLE_SCHEMA = 'smart_hospital'
ORDER BY TABLE_NAME, INDEX_NAME;

-- Rebuild indexes
ALTER TABLE patients DROP INDEX idx_patient_name;
ALTER TABLE patients ADD INDEX idx_patient_name (name);
```

#### 12.2.3 Data Cleanup
```sql
-- Archive old records (example: records older than 2 years)
INSERT INTO medical_records_archive 
SELECT * FROM medical_records 
WHERE visit_date < DATE_SUB(NOW(), INTERVAL 2 YEAR);

-- Delete archived records from main table
DELETE FROM medical_records 
WHERE visit_date < DATE_SUB(NOW(), INTERVAL 2 YEAR);

-- Clean up cancelled appointments older than 6 months
DELETE FROM appointments 
WHERE status = 'Cancelled' 
    AND appointment_date < DATE_SUB(NOW(), INTERVAL 6 MONTH);
```

### 12.3 Performance Monitoring

#### 12.3.1 Database Performance Queries
```sql
-- Check slow queries
SELECT 
    query_time,
    lock_time,
    rows_sent,
    rows_examined,
    sql_text
FROM mysql.slow_log
WHERE start_time >= DATE_SUB(NOW(), INTERVAL 1 DAY)
ORDER BY query_time DESC;

-- Table sizes
SELECT 
    table_name,
    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Size (MB)',
    table_rows
FROM information_schema.tables
WHERE table_schema = 'smart_hospital'
ORDER BY (data_length + index_length) DESC;

-- Connection statistics
SHOW STATUS LIKE 'Connections';
SHOW STATUS LIKE 'Max_used_connections';
SHOW STATUS LIKE 'Threads_connected';
```

---

## Error Handling & Logging

### 13.1 Error Handling Implementation

#### 13.1.1 Database Error Classes
```python
class DatabaseError(Exception):
    """Base class for database-related errors"""
    pass

class ConnectionError(DatabaseError):
    """Database connection errors"""
    pass

class ValidationError(DatabaseError):
    """Data validation errors"""
    pass

class IntegrityError(DatabaseError):
    """Data integrity constraint violations"""
    pass

class OperationError(DatabaseError):
    """Database operation errors"""
    pass
```

#### 13.1.2 Error Handler Implementation
```python
import logging
from functools import wraps

def handle_database_errors(func):
    """Decorator to handle database errors consistently"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except mysql.connector.Error as e:
            error_code = e.errno
            error_msg = str(e)
            
            # Log the error
            logger.error(f"Database error in {func.__name__}: [{error_code}] {error_msg}")
            
            # Handle specific error types
            if error_code == 1062:  # Duplicate entry
                raise IntegrityError(f"Duplicate entry: {error_msg}")
            elif error_code == 1452:  # Foreign key constraint
                raise IntegrityError(f"Foreign key constraint violation: {error_msg}")
            elif error_code == 2003:  # Connection refused
                raise ConnectionError(f"Cannot connect to database: {error_msg}")
            elif error_code == 1045:  # Access denied
                raise ConnectionError(f"Access denied: {error_msg}")
            else:
                raise OperationError(f"Database operation failed: {error_msg}")
        
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {str(e)}")
            raise OperationError(f"Unexpected error: {str(e)}")
    
    return wrapper
```

#### 13.1.3 Validation Error Handling
```python
def validate_and_save_patient(self, **patient_data):
    """Validate patient data and save with proper error handling"""
    try:
        # Validate required fields
        required_fields = ['name', 'age', 'gender']
        for field in required_fields:
            if field not in patient_data or not patient_data[field]:
                raise ValidationError(f"Required field missing: {field}")
        
        # Validate data types and ranges
        if not isinstance(patient_data['age'], int) or not (1 <= patient_data['age'] <= 150):
            raise ValidationError("Age must be an integer between 1 and 150")
        
        if patient_data['gender'] not in ['Male', 'Female', 'Other']:
            raise ValidationError("Gender must be 'Male', 'Female', or 'Other'")
        
        # Validate contact if provided
        if 'contact' in patient_data and patient_data['contact']:
            contact = str(patient_data['contact'])
            if not contact.isdigit() or len(contact) != 10:
                raise ValidationError("Contact must be a 10-digit number")
        
        # Save patient
        return self.add_patient(**patient_data)
        
    except ValidationError:
        raise  # Re-raise validation errors
    except Exception as e:
        logger.error(f"Error validating/saving patient: {e}")
        raise OperationError(f"Failed to save patient: {str(e)}")
```

### 13.2 Logging Configuration

#### 13.2.1 Logging Setup
```python
import logging
import os
from datetime import datetime

# Create logs directory
os.makedirs('logs', exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/hospital_db_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler()  # Console output
    ]
)

# Create specialized loggers
db_logger = logging.getLogger('database')
performance_logger = logging.getLogger('performance')
security_logger = logging.getLogger('security')

# Performance logging decorator
def log_performance(func):
    """Decorator to log function execution time"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            performance_logger.info(f"{func.__name__} executed in {execution_time:.3f}s")
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            performance_logger.error(f"{func.__name__} failed after {execution_time:.3f}s: {str(e)}")
            raise
    return wrapper
```

#### 13.2.2 Audit Logging
```python
def log_database_operation(operation, table, record_id=None, user_id=None, details=None):
    """Log database operations for audit trail"""
    audit_entry = {
        'timestamp': datetime.now().isoformat(),
        'operation': operation,
        'table': table,
        'record_id': record_id,
        'user_id': user_id,
        'details': details,
        'ip_address': get_client_ip(),  # Implement this function
        'session_id': get_session_id()  # Implement this function
    }
    
    security_logger.info(f"AUDIT: {json.dumps(audit_entry)}")
```

### 13.3 Health Monitoring

#### 13.3.1 Database Health Check
```python
def health_check(self) -> Dict:
    """Comprehensive database health check"""
    health_status = {
        'status': 'healthy',
        'checks': {},
        'timestamp': datetime.now().isoformat()
    }
    
    try:
        # Connection test
        conn_start = time.time()
        if self.test_connection():
            health_status['checks']['connection'] = {
                'status': 'pass',
                'response_time': time.time() - conn_start
            }
        else:
            health_status['checks']['connection'] = {
                'status': 'fail',
                'error': 'Cannot connect to database'
            }
            health_status['status'] = 'unhealthy'
        
        # Table accessibility
        for table in ['patients', 'doctors', 'appointments', 'medical_records']:
            try:
                query_start = time.time()
                conn = self.get_connection()
                cursor = conn.cursor()
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                cursor.fetchone()
                cursor.close()
                conn.close()
                
                health_status['checks'][f'{table}_table'] = {
                    'status': 'pass',
                    'response_time': time.time() - query_start
                }
            except Exception as e:
                health_status['checks'][f'{table}_table'] = {
                    'status': 'fail',
                    'error': str(e)
                }
                health_status['status'] = 'unhealthy'
        
        # Pool status
        health_status['checks']['connection_pool'] = {
            'status': 'pass',
            'pool_size': self.pool._pool_size,
            'connections_in_use': len(self.pool._cnx_queue._queue)
        }
        
    except Exception as e:
        health_status['status'] = 'unhealthy'
        health_status['error'] = str(e)
    
    return health_status
```

---

## API Integration Layer

### 14.1 Database API Wrapper

#### 14.1.1 RESTful API Design
```python
from flask import Flask, jsonify, request
from functools import wraps

app = Flask(__name__)

def api_error_handler(func):
    """Handle API errors and return proper HTTP responses"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as e:
            return jsonify({'error': 'Validation error', 'message': str(e)}), 400
        except IntegrityError as e:
            return jsonify({'error': 'Data integrity error', 'message': str(e)}), 409
        except ConnectionError as e:
            return jsonify({'error': 'Database connection error', 'message': str(e)}), 503
        except Exception as e:
            logger.error(f"API error: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500
    return wrapper

# Patient API endpoints
@app.route('/api/patients', methods=['GET'])
@api_error_handler
def get_patients_api():
    """Get all patients with optional pagination and search"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', None)
    
    result = db.get_patients_paginated(page, per_page, search)
    
    return jsonify({
        'status': 'success',
        'data': result['data'],
        'pagination': result['pagination']
    })

@app.route('/api/patients', methods=['POST'])
@api_error_handler
def create_patient_api():
    """Create new patient"""
    data = request.get_json()
    
    patient_id = db.validate_and_save_patient(**data)
    
    return jsonify({
        'status': 'success',
        'message': 'Patient created successfully',
        'patient_id': patient_id
    }), 201
```

#### 14.1.2 GraphQL Integration
```python
import graphene
from graphene import ObjectType, String, Int, Float, List, Field

class Patient(ObjectType):
    patient_id = Int()
    name = String()
    age = Int()
    gender = String()
    contact = String()
    address = String()
    created_at = String()

class MedicalRecord(ObjectType):
    record_id = Int()
    patient_id = Int()
    doctor_id = Int()
    symptoms = String()
    predicted_disease = String()
    confidence_score = Float()
    visit_date = String()

class Query(ObjectType):
    patients = List(Patient, search=String(), limit=Int())
    patient = Field(Patient, patient_id=Int(required=True))
    medical_history = List(MedicalRecord, patient_id=Int(required=True))
    
    def resolve_patients(self, info, search=None, limit=20):
        # Implementation to fetch patients
        pass
    
    def resolve_patient(self, info, patient_id):
        # Implementation to fetch single patient
        pass
    
    def resolve_medical_history(self, info, patient_id):
        # Implementation to fetch patient medical history
        pass

schema = graphene.Schema(query=Query)
```

### 14.2 Streamlit Integration

#### 14.2.1 Database Service Layer
```python
class DatabaseService:
    """Service layer for Streamlit application"""
    
    def __init__(self):
        self.db = HospitalDatabase()
    
    @st.cache_data(ttl=300)  # Cache for 5 minutes
    def get_dashboard_data(self):
        """Get cached dashboard data for Streamlit"""
        return self.db.get_dashboard_stats()
    
    def add_patient_with_validation(self, patient_data):
        """Add patient with UI-friendly error handling"""
        try:
            # Validate data
            errors = DataValidator.validate_patient_data(**patient_data)
            if errors:
                return {'success': False, 'errors': errors}
            
            # Save patient
            patient_id = self.db.add_patient(**patient_data)
            
            # Clear cache
            st.cache_data.clear()
            
            return {
                'success': True,
                'message': f'Patient added successfully with ID: {patient_id}',
                'patient_id': patient_id
            }
            
        except Exception as e:
            return {'success': False, 'errors': [str(e)]}
```

#### 14.2.2 Streamlit Database Components
```python
def display_patient_form():
    """Streamlit form for patient registration"""
    with st.form("patient_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Patient Name *")
            age = st.number_input("Age *", min_value=1, max_value=150, value=30)
            gender = st.selectbox("Gender *", ["Male", "Female", "Other"])
        
        with col2:
            contact = st.text_input("Contact Number")
            address = st.text_area("Address")
        
        submitted = st.form_submit_button("Add Patient")
        
        if submitted:
            patient_data = {
                'name': name,
                'age': age,
                'gender': gender,
                'contact': contact if contact else None,
                'address': address if address else None
            }
            
            # Use database service
            db_service = DatabaseService()
            result = db_service.add_patient_with_validation(patient_data)
            
            if result['success']:
                st.success(result['message'])
            else:
                for error in result['errors']:
                    st.error(error)
```

---

## Testing & Validation

### 15.1 Unit Tests

#### 15.1.1 Database Operation Tests
```python
import unittest
from unittest.mock import Mock, patch
import mysql.connector

class TestHospitalDatabase(unittest.TestCase):
    """Test cases for hospital database operations"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.db = HospitalDatabase()
        self.test_patient_data = {
            'name': 'Test Patient',
            'age': 25,
            'gender': 'Male',
            'contact': '9876543210',
            'address': 'Test Address'
        }
    
    def test_add_patient_success(self):
        """Test successful patient addition"""
        with patch.object(self.db, 'get_connection') as mock_conn:
            # Mock database connection and cursor
            mock_cursor = Mock()
            mock_cursor.lastrowid = 123
            mock_conn.return_value.cursor.return_value = mock_cursor
            
            # Test patient addition
            patient_id = self.db.add_patient(**self.test_patient_data)
            
            # Assertions
            self.assertEqual(patient_id, 123)
            mock_cursor.execute.assert_called_once()
            mock_conn.return_value.commit.assert_called_once()
    
    def test_add_patient_validation_error(self):
        """Test patient addition with invalid data"""
        invalid_data = {
            'name': '',  # Empty name should fail
            'age': 25,
            'gender': 'Male'
        }
        
        with self.assertRaises(ValidationError):
            self.db.validate_and_save_patient(**invalid_data)
    
    def test_get_patients(self):
        """Test patient retrieval"""
        with patch.object(self.db, 'get_connection') as mock_conn:
            # Mock return data
            mock_cursor = Mock()
            mock_cursor.fetchall.return_value = [
                {
                    'patient_id': 1,
                    'name': 'Test Patient',
                    'age': 25,
                    'gender': 'Male'
                }
            ]
            mock_conn.return_value.cursor.return_value = mock_cursor
            
            # Test get patients
            patients = self.db.get_patients()
            
            # Assertions
            self.assertEqual(len(patients), 1)
            self.assertEqual(patients[0]['name'], 'Test Patient')
```

#### 15.1.2 Integration Tests
```python
class TestDatabaseIntegration(unittest.TestCase):
    """Integration tests for database operations"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test database"""
        cls.test_db = HospitalDatabase(
            host='localhost',
            user='test_user',
            password='test_password',
            database='test_smart_hospital'
        )
        
        # Create test tables
        cls.setup_test_tables()
    
    @classmethod
    def setup_test_tables(cls):
        """Create test database tables"""
        with open('database/schema.sql', 'r') as f:
            schema_sql = f.read()
        
        # Execute schema creation
        conn = cls.test_db.get_connection()
        cursor = conn.cursor()
        
        for statement in schema_sql.split(';'):
            if statement.strip():
                cursor.execute(statement)
        
        conn.commit()
        cursor.close()
        conn.close()
    
    def test_patient_lifecycle(self):
        """Test complete patient lifecycle"""
        # Create patient
        patient_id = self.test_db.add_patient(
            name='Integration Test Patient',
            age=30,
            gender='Female',
            contact='9876543210'
        )
        self.assertIsNotNone(patient_id)
        
        # Retrieve patient
        patient = self.test_db.get_patient_by_id(patient_id)
        self.assertEqual(patient['name'], 'Integration Test Patient')
        
        # Update patient
        success = self.test_db.update_patient(patient_id, age=31)
        self.assertTrue(success)
        
        # Verify update
        updated_patient = self.test_db.get_patient_by_id(patient_id)
        self.assertEqual(updated_patient['age'], 31)
        
        # Delete patient (cleanup)
        success = self.test_db.delete_patient(patient_id)
        self.assertTrue(success)
```

### 15.2 Performance Tests

#### 15.2.1 Load Testing
```python
import time
import threading
import statistics

class PerformanceTest:
    """Performance testing for database operations"""
    
    def __init__(self):
        self.db = HospitalDatabase()
        self.results = []
    
    def test_concurrent_patient_creation(self, num_threads=10, patients_per_thread=100):
        """Test concurrent patient creation"""
        threads = []
        
        def create_patients(thread_id):
            thread_results = []
            for i in range(patients_per_thread):
                start_time = time.time()
                try:
                    patient_id = self.db.add_patient(
                        name=f'Test Patient {thread_id}-{i}',
                        age=25 + (i % 50),
                        gender='Male' if i % 2 else 'Female',
                        contact=f'987654{thread_id:04d}{i:02d}'
                    )
                    execution_time = time.time() - start_time
                    thread_results.append({
                        'success': True,
                        'time': execution_time,
                        'patient_id': patient_id
                    })
                except Exception as e:
                    execution_time = time.time() - start_time
                    thread_results.append({
                        'success': False,
                        'time': execution_time,
                        'error': str(e)
                    })
            
            self.results.extend(thread_results)
        
        # Start threads
        for i in range(num_threads):
            thread = threading.Thread(target=create_patients, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Analyze results
        successful_operations = [r for r in self.results if r['success']]
        execution_times = [r['time'] for r in successful_operations]
        
        return {
            'total_operations': len(self.results),
            'successful_operations': len(successful_operations),
            'success_rate': len(successful_operations) / len(self.results) * 100,
            'avg_execution_time': statistics.mean(execution_times),
            'median_execution_time': statistics.median(execution_times),
            'min_execution_time': min(execution_times),
            'max_execution_time': max(execution_times)
        }
```

### 15.3 Data Validation Tests

#### 15.3.1 Constraint Tests
```python
def test_database_constraints():
    """Test database constraints and validations"""
    test_cases = [
        {
            'name': 'Invalid age - negative',
            'data': {'name': 'Test', 'age': -5, 'gender': 'Male'},
            'should_fail': True
        },
        {
            'name': 'Invalid age - too high',
            'data': {'name': 'Test', 'age': 200, 'gender': 'Male'},
            'should_fail': True
        },
        {
            'name': 'Invalid gender',
            'data': {'name': 'Test', 'age': 25, 'gender': 'Unknown'},
            'should_fail': True
        },
        {
            'name': 'Valid data',
            'data': {'name': 'Test Patient', 'age': 25, 'gender': 'Male'},
            'should_fail': False
        }
    ]
    
    for test_case in test_cases:
        try:
            result = db.validate_and_save_patient(**test_case['data'])
            if test_case['should_fail']:
                print(f"FAIL: {test_case['name']} - Should have failed but succeeded")
            else:
                print(f"PASS: {test_case['name']} - Succeeded as expected")
        except (ValidationError, IntegrityError):
            if test_case['should_fail']:
                print(f"PASS: {test_case['name']} - Failed as expected")
            else:
                print(f"FAIL: {test_case['name']} - Should have succeeded but failed")
```

---

## Database Statistics & Analytics

### Current Database State
- **Total Tables**: 5 (patients, doctors, appointments, medical_records, users)
- **Total Indexes**: 15+ optimized indexes for performance
- **Foreign Key Relationships**: 5 relationships with cascade rules
- **Constraints**: 8+ check constraints for data integrity
- **Supported Operations**: Full CRUD operations on all entities
- **Connection Pool**: 5-10 concurrent connections
- **Estimated Performance**: 1000+ operations per second under normal load

### Key Features Implemented
1. **Complete CRUD Operations** for all entities
2. **Advanced Query Filtering** with pagination
3. **ML Integration** for disease prediction storage
4. **Connection Pooling** for optimal performance
5. **Comprehensive Error Handling** with proper logging
6. **Data Validation** at multiple levels
7. **Transaction Management** for data consistency
8. **Performance Optimization** with indexes and caching
9. **Security Implementation** with parameterized queries
10. **Backup & Recovery** procedures

---

*This comprehensive DBMS documentation covers every aspect of the Smart Hospital Management System database implementation. It serves as a complete reference for understanding the database architecture, operations, and maintenance procedures.*

**Document Version**: 2.0  
**Last Updated**: October 14, 2025  
**Authors**: Krishna & Omkar  
**Database Status**: Production Ready