from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class FamilyInfo:
    id: int
    patient_id: int
    patient_type: str  # 'student' or 'veteran'
    father_name: str
    mother_name: str
    birth_order: int
    occupation: str
    caregiver_info: str
    
@dataclass
class User:
    id: int
    username: str
    password_hash: str
    role: str
    full_name: str
    email: str  # Added email field
    created_at: datetime

@dataclass
class Student:
    id: int
    full_name: str
    birth_date: datetime
    address: str
    email: str  # Added email field
    admission_date: datetime
    health_status: str
    academic_status: str
    psychological_status: str
    profile_image: Optional[bytes] = None

@dataclass
class Veteran:
    id: int
    full_name: str
    birth_date: datetime
    service_period: str
    health_condition: str
    address: str
    email: str  # Added email field
    contact_info: str
    profile_image: Optional[bytes] = None

@dataclass
class MedicalRecord:
    id: int
    patient_id: int
    patient_type: str  # 'student' or 'veteran'
    diagnosis: str
    treatment: str
    doctor_id: int
    date: datetime
    notes: Optional[str]
    notification_sent: bool  # Added notification tracking

@dataclass
class PsychologicalEvaluation:
    id: int
    student_id: int
    evaluation_date: datetime
    evaluator_id: int
    assessment: str
    recommendations: str
    follow_up_date: Optional[datetime]
    notification_sent: bool  # Added notification tracking