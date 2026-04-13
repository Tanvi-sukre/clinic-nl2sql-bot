import sqlite3
import random
from datetime import datetime, timedelta

def setup_database():
    conn = sqlite3.connect('clinic.db')
    cursor = conn.cursor()

    # Create Tables 
    cursor.execute('''CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT,
        phone TEXT,
        date_of_birth DATE,
        gender TEXT,
        city TEXT,
        registered_date DATE
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        specialization TEXT,
        department TEXT,
        phone TEXT
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        doctor_id INTEGER,
        appointment_date DATETIME,
        status TEXT,
        notes TEXT,
        FOREIGN KEY(patient_id) REFERENCES patients(id),
        FOREIGN KEY(doctor_id) REFERENCES doctors(id)
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS treatments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        appointment_id INTEGER,
        treatment_name TEXT,
        cost REAL,
        duration_minutes INTEGER,
        FOREIGN KEY(appointment_id) REFERENCES appointments(id)
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS invoices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        invoice_date DATE,
        total_amount REAL,
        paid_amount REAL,
        status TEXT,
        FOREIGN KEY(patient_id) REFERENCES patients(id)
    )''')

    # Insert 15 Doctors
    specs = ['Dermatology', 'Cardiology', 'Orthopedics', 'General', 'Pediatrics']
    doctors_data = []
    for i in range(15):
        spec = random.choice(specs)
        doctors_data.append((f"Dr. Smith {i}", spec, f"{spec} Dept", f"555-010{i}"))
    cursor.executemany('INSERT INTO doctors (name, specialization, department, phone) VALUES (?,?,?,?)', doctors_data)

    # Insert 200 Patients 
    cities = ['Mumbai', 'Delhi', 'Bangalore', 'Thane', 'Pune', 'Chennai', 'Kolkata', 'Hyderabad']
    patients_data = []
    for i in range(200):
        gender = random.choice(['M', 'F'])
        patients_data.append((f"Patient_{i}", "Surname", f"p{i}@email.com", f"999-{i:04d}", "1990-01-01", gender, random.choice(cities), "2025-01-01"))
    cursor.executemany('INSERT INTO patients (first_name, last_name, email, phone, date_of_birth, gender, city, registered_date) VALUES (?,?,?,?,?,?,?,?)', patients_data)

    # Insert 500 Appointments 
    statuses = ['Completed', 'Scheduled', 'Cancelled', 'No-Show']
    for _ in range(500):
        p_id = random.randint(1, 200)
        d_id = random.randint(1, 15)
        # Random date in the last 12 months 
        random_days = random.randint(0, 365)
        appt_date = (datetime.now() - timedelta(days=random_days)).strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('INSERT INTO appointments (patient_id, doctor_id, appointment_date, status) VALUES (?,?,?,?)', 
                       (p_id, d_id, appt_date, random.choice(statuses)))

    conn.commit()
    print(f"Database created successfully: clinic.db ")
    conn.close()

if __name__ == "__main__":
    setup_database()
