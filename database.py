import sqlite3
from typing import List, Optional
from datetime import datetime
import hashlib
from models import User, Student, Veteran, MedicalRecord, PsychologicalEvaluation

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('lang_huu_nghi.db', check_same_thread=False)
        self.create_tables()
        self.create_initial_admin()  # Add this line

    def create_tables(self):
        cursor = self.conn.cursor()

        # Users table with email
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            full_name TEXT NOT NULL,
            email TEXT,  -- Added email field
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        # Students table with email
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            full_name TEXT NOT NULL,
            birth_date DATE NOT NULL,
            address TEXT,
            email TEXT,  -- Added email field
            admission_date DATE NOT NULL,
            health_status TEXT,
            academic_status TEXT,
            psychological_status TEXT
        )
        ''')

        # Veterans table with email
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS veterans (
            id INTEGER PRIMARY KEY,
            full_name TEXT NOT NULL,
            birth_date DATE NOT NULL,
            service_period TEXT,
            health_condition TEXT,
            address TEXT,
            email TEXT,  -- Added email field
            contact_info TEXT
        )
        ''')

        # Medical records table with notification tracking
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
            notification_sent BOOLEAN DEFAULT FALSE,  -- Added notification tracking
            FOREIGN KEY (doctor_id) REFERENCES users (id)
        )
        ''')

        # Psychological evaluations table with notification tracking
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS psychological_evaluations (
            id INTEGER PRIMARY KEY,
            student_id INTEGER NOT NULL,
            evaluation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            evaluator_id INTEGER NOT NULL,
            assessment TEXT,
            recommendations TEXT,
            follow_up_date DATE,
            notification_sent BOOLEAN DEFAULT FALSE,  -- Added notification tracking
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

    def send_medical_record_notification(self, record_id: int) -> bool:
        """Send notification for medical record and update notification status."""
        cursor = self.conn.cursor()
        try:
            # Get record details
            cursor.execute("""
                SELECT mr.*, u.full_name as doctor_name,
                CASE 
                    WHEN mr.patient_type = 'student' THEN s.email
                    WHEN mr.patient_type = 'veteran' THEN v.email
                END as patient_email
                FROM medical_records mr
                JOIN users u ON mr.doctor_id = u.id
                LEFT JOIN students s ON mr.patient_id = s.id AND mr.patient_type = 'student'
                LEFT JOIN veterans v ON mr.patient_id = v.id AND mr.patient_type = 'veteran'
                WHERE mr.id = ?
            """, (record_id,))
            record = cursor.fetchone()

            if record and record[-1]:  # If we have patient email
                from email_utils import send_medical_notification
                success = send_medical_notification(
                    patient_email=record[-1],
                    appointment_date=record[6].strftime("%Y-%m-%d %H:%M"),
                    doctor_name=record[-2]
                )
                if success:
                    cursor.execute(
                        "UPDATE medical_records SET notification_sent = TRUE WHERE id = ?",
                        (record_id,)
                    )
                    self.conn.commit()
                return success
        except Exception as e:
            print(f"Error sending medical notification: {e}")
            return False
        return False

    def send_psychological_evaluation_notification(self, eval_id: int) -> bool:
        """Send notification for psychological evaluation and update notification status."""
        cursor = self.conn.cursor()
        try:
            # Get evaluation details
            cursor.execute("""
                SELECT pe.*, u.full_name as counselor_name, s.email as student_email
                FROM psychological_evaluations pe
                JOIN users u ON pe.evaluator_id = u.id
                JOIN students s ON pe.student_id = s.id
                WHERE pe.id = ?
            """, (eval_id,))
            eval_record = cursor.fetchone()

            if eval_record and eval_record[-1]:  # If we have student email
                from email_utils import send_psychological_notification
                success = send_psychological_notification(
                    student_email=eval_record[-1],
                    evaluation_date=eval_record[2].strftime("%Y-%m-%d %H:%M"),
                    counselor_name=eval_record[-2]
                )
                if success:
                    cursor.execute(
                        "UPDATE psychological_evaluations SET notification_sent = TRUE WHERE id = ?",
                        (eval_id,)
                    )
                    self.conn.commit()
                return success
        except Exception as e:
            print(f"Error sending psychological notification: {e}")
            return False
        return False

    def create_initial_admin(self):
        """Create an initial admin user if no users exist."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]

        if user_count == 0:
            # Create default admin user
            username = "admin"
            password = "admin123"
            password_hash = hashlib.sha256(password.encode()).hexdigest()

            cursor.execute("""
                INSERT INTO users (username, password_hash, role, full_name, email)
                VALUES (?, ?, ?, ?, ?)
            """, (username, password_hash, "admin", "System Administrator", "admin@langhunghi.edu.vn"))
            self.conn.commit()
            return True
        return False