import sqlite3
from typing import List, Optional
from datetime import datetime
import hashlib
from models import User, Student, Veteran, MedicalRecord, PsychologicalEvaluation

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('lang_huu_nghi.db', check_same_thread=False)
        self.create_tables()
        self.create_initial_admin()
        self.create_sample_data()  
    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Family info table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS family_info (
            id INTEGER PRIMARY KEY,
            patient_id INTEGER NOT NULL,
            patient_type TEXT NOT NULL,
            father_name TEXT,
            mother_name TEXT,
            birth_order INTEGER,
            occupation TEXT,
            caregiver_info TEXT
        )
        ''')

        # Users table with email
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            full_name TEXT NOT NULL,
            email TEXT,  
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        # Students table with email and image
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            full_name TEXT NOT NULL,
            birth_date DATE NOT NULL,
            address TEXT,
            email TEXT,  
            admission_date DATE NOT NULL,
            health_status TEXT,
            academic_status TEXT,
            psychological_status TEXT,
            profile_image BLOB
        )
        ''')

        # Veterans table with email and image
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS veterans (
            id INTEGER PRIMARY KEY,
            full_name TEXT NOT NULL,
            birth_date DATE NOT NULL,
            service_period TEXT,
            health_condition TEXT,
            address TEXT,
            email TEXT,  
            contact_info TEXT,
            profile_image BLOB
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
            notification_sent BOOLEAN DEFAULT FALSE,  
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
            notification_sent BOOLEAN DEFAULT FALSE,  
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

    def create_sample_data(self):
        """Create sample data for testing and demonstration."""
        cursor = self.conn.cursor()

        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] > 1:  # If we have more than just admin
            return False

        # Create sample users
        users = [
            ("doctor1", "password123", "doctor", "Bác sĩ Nguyễn Văn A", "doctor1@langhunghi.edu.vn"),
            ("doctor2", "password123", "doctor", "Bác sĩ Trần Thị B", "doctor2@langhunghi.edu.vn"),
            ("teacher1", "password123", "teacher", "Giáo viên Phạm Văn C", "teacher1@langhunghi.edu.vn"),
            ("counselor1", "password123", "counselor", "Tư vấn Lê Thị D", "counselor1@langhunghi.edu.vn")
        ]

        for username, password, role, full_name, email in users:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            cursor.execute("""
                INSERT INTO users (username, password_hash, role, full_name, email)
                VALUES (?, ?, ?, ?, ?)
            """, (username, password_hash, role, full_name, email))

        # Create sample students
        students = [
            ("Nguyễn Văn Học", "2000-01-15", "Hà Nội", "student1@langhunghi.edu.vn", "2023-09-01", "Good", "Excellent"),
            ("Trần Thị Mai", "2001-03-20", "Hải Phòng", "student2@langhunghi.edu.vn", "2023-09-01", "Fair", "Good"),
            ("Lê Văn Nam", "2000-07-10", "Đà Nẵng", "student3@langhunghi.edu.vn", "2023-09-01", "Needs Attention", "Average")
        ]

        for name, birth, addr, email, admission, health, academic in students:
            cursor.execute("""
                INSERT INTO students (full_name, birth_date, address, email, admission_date, health_status, academic_status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (name, birth, addr, email, admission, health, academic))

        # Create sample veterans
        veterans = [
            ("Phạm Văn Chiến", "1960-05-20", "1980-1985", "Good", "Hà Nội", "veteran1@langhunghi.edu.vn", "0912345678"),
            ("Nguyễn Thị Hòa", "1965-11-15", "1985-1990", "Fair", "Hồ Chí Minh", "veteran2@langhunghi.edu.vn", "0923456789")
        ]

        for name, birth, service, health, addr, email, contact in veterans:
            cursor.execute("""
                INSERT INTO veterans (full_name, birth_date, service_period, health_condition, address, email, contact_info)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (name, birth, service, health, addr, email, contact))

        # Create sample medical records
        medical_records = [
            (1, "student", "Cảm cúm thông thường", "Nghỉ ngơi và uống thuốc", 2, "Cần theo dõi"),
            (2, "student", "Đau đầu", "Thuốc giảm đau", 2, "Tái khám sau 1 tuần"),
            (1, "veteran", "Đau lưng mãn tính", "Vật lý trị liệu", 3, "Cần tập thể dục thường xuyên")
        ]

        for patient_id, type, diagnosis, treatment, doctor_id, notes in medical_records:
            cursor.execute("""
                INSERT INTO medical_records (patient_id, patient_type, diagnosis, treatment, doctor_id, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (patient_id, type, diagnosis, treatment, doctor_id, notes))

        # Create sample psychological evaluations
        evaluations = [
            (1, "Thích nghi tốt với môi trường học tập", "Tiếp tục theo dõi", "2024-04-01"),
            (2, "Lo âu nhẹ về học tập", "Cần tư vấn định kỳ", "2024-03-20"),
            (3, "Khó khăn trong giao tiếp", "Tham gia các hoạt động nhóm", "2024-03-25")
        ]

        for student_id, assessment, recommendations, follow_up in evaluations:
            cursor.execute("""
                INSERT INTO psychological_evaluations (student_id, evaluator_id, assessment, recommendations, follow_up_date)
                VALUES (?, ?, ?, ?, ?)
            """, (student_id, 5, assessment, recommendations, follow_up))  # counselor1 has ID 5

        self.conn.commit()
        return True
    
    def update_tables_for_images(self):
        cursor = self.conn.cursor()

        # Add image column to students table
        cursor.execute('''
        ALTER TABLE students
        ADD COLUMN profile_image BLOB
        ''')

        # Add image column to veterans table
        cursor.execute('''
        ALTER TABLE veterans 
        ADD COLUMN profile_image BLOB
        ''')

        self.conn.commit()

    def save_student_image(self, student_id: int, image_data: bytes) -> bool:
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "UPDATE students SET profile_image = ? WHERE id = ?",
                (image_data, student_id)
            )
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error saving student image: {e}")
            return False

    def save_veteran_image(self, veteran_id: int, image_data: bytes) -> bool:
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "UPDATE veterans SET profile_image = ? WHERE id = ?",
                (image_data, veteran_id)
            )
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error saving veteran image: {e}")
            return False

    def get_student_image(self, student_id: int) -> Optional[bytes]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT profile_image FROM students WHERE id = ?", (student_id,))
        result = cursor.fetchone()
        return result[0] if result else None

    def get_veteran_image(self, veteran_id: int) -> Optional[bytes]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT profile_image FROM veterans WHERE id = ?", (veteran_id,))
        result = cursor.fetchone()
        return result[0] if result else None
        
    def add_family_info(self, family_info: dict) -> int:
        """Add family information for a patient"""
        cursor = self.conn.cursor()
        cursor.execute(
            """INSERT INTO family_info 
            (patient_id, patient_type, father_name, mother_name, birth_order, occupation, caregiver_info)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (family_info["patient_id"], family_info["patient_type"], family_info["father_name"],
             family_info["mother_name"], family_info["birth_order"], 
             family_info["occupation"], family_info["caregiver_info"])
        )
        self.conn.commit()
        return cursor.lastrowid
        
    def get_family_info(self, patient_id: int, patient_type: str) -> Optional[dict]:
        """Get family information for a patient"""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM family_info WHERE patient_id = ? AND patient_type = ?",
            (patient_id, patient_type)
        )
        result = cursor.fetchone()
        if result:
            return {
                "id": result[0],
                "patient_id": result[1],
                "patient_type": result[2],
                "father_name": result[3],
                "mother_name": result[4],
                "birth_order": result[5],
                "occupation": result[6],
                "caregiver_info": result[7]
            }
        return None
        
    def update_family_info(self, family_id: int, family_info: dict) -> bool:
        """Update family information"""
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                """UPDATE family_info 
                SET father_name = ?, mother_name = ?, birth_order = ?, 
                occupation = ?, caregiver_info = ?
                WHERE id = ?""",
                (family_info["father_name"], family_info["mother_name"], 
                 family_info["birth_order"], family_info["occupation"], 
                 family_info["caregiver_info"], family_id)
            )
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error updating family info: {e}")
            return False