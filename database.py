import sqlite3
from typing import List, Optional
from datetime import datetime
import hashlib
from models import User, Student, Veteran, MedicalRecord, PsychologicalEvaluation

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('lang_huu_nghi.db', check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            full_name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        # Students table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            full_name TEXT NOT NULL,
            birth_date DATE NOT NULL,
            address TEXT,
            admission_date DATE NOT NULL,
            health_status TEXT,
            academic_status TEXT,
            psychological_status TEXT
        )
        ''')

        # Veterans table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS veterans (
            id INTEGER PRIMARY KEY,
            full_name TEXT NOT NULL,
            birth_date DATE NOT NULL,
            service_period TEXT,
            health_condition TEXT,
            address TEXT,
            contact_info TEXT
        )
        ''')

        # Medical records table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS medical_records (
            id INTEGER PRIMARY KEY,
            patient_id INTEGER NOT NULL,
            patient_type TEXT NOT NULL,
            diagnosis TEXT,
            treatment TEXT,
            doctor_id INTEGER NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            notes TEXT,
            FOREIGN KEY (doctor_id) REFERENCES users (id)
        )
        ''')

        # Psychological evaluations table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS psychological_evaluations (
            id INTEGER PRIMARY KEY,
            student_id INTEGER NOT NULL,
            evaluation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            evaluator_id INTEGER NOT NULL,
            assessment TEXT,
            recommendations TEXT,
            follow_up_date DATE,
            FOREIGN KEY (student_id) REFERENCES students (id),
            FOREIGN KEY (evaluator_id) REFERENCES users (id)
        )
        ''')

        self.conn.commit()

    def get_user_by_username(self, username: str) -> Optional[User]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        if result:
            return User(*result)
        return None

    def add_user(self, username: str, password: str, role: str, full_name: str) -> bool:
        try:
            cursor = self.conn.cursor()
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            cursor.execute(
                "INSERT INTO users (username, password_hash, role, full_name) VALUES (?, ?, ?, ?)",
                (username, password_hash, role, full_name)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_students(self) -> List[Student]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM students")
        return [Student(*row) for row in cursor.fetchall()]

    def get_veterans(self) -> List[Veteran]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM veterans")
        return [Veteran(*row) for row in cursor.fetchall()]

    def add_medical_record(self, record: MedicalRecord) -> int:
        cursor = self.conn.cursor()
        cursor.execute(
            """INSERT INTO medical_records 
            (patient_id, patient_type, diagnosis, treatment, doctor_id, notes)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (record.patient_id, record.patient_type, record.diagnosis,
             record.treatment, record.doctor_id, record.notes)
        )
        self.conn.commit()
        return cursor.lastrowid

    def add_psychological_evaluation(self, eval: PsychologicalEvaluation) -> int:
        cursor = self.conn.cursor()
        cursor.execute(
            """INSERT INTO psychological_evaluations 
            (student_id, evaluator_id, assessment, recommendations, follow_up_date)
            VALUES (?, ?, ?, ?, ?)""",
            (eval.student_id, eval.evaluator_id, eval.assessment,
             eval.recommendations, eval.follow_up_date)
        )
        self.conn.commit()
        return cursor.lastrowid
