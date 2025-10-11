CREATE TABLE doctors (
    doctor_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    specialization VARCHAR(100),
    contact VARCHAR(15)
);

CREATE TABLE patients (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    gender VARCHAR(10),
    symptoms TEXT
);

CREATE TABLE appointments (
    appointment_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    doctor_id INT,
    date DATETIME,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
);

CREATE TABLE predictions (
    prediction_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    predicted_disease VARCHAR(100),
    confidence FLOAT,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
