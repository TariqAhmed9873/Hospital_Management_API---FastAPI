from sqlalchemy import Boolean, Column, String, Integer, DateTime, Time
from database import Base
from datetime import datetime


# model for patient
class Patient(Base):
    __tablename__ = "patient"

    patient_id = Column(Integer, primary_key=True, index=True) #patient_id
    full_name = Column(String)
    gender = Column(String)
    date_of_birth = Column(DateTime)
    blood_group = Column(String)
    phone_number = Column(String(15))
    email = Column(String)
    address = Column(String)
    emergency_contact = Column(String(15))
    registration_date = Column(DateTime, default=datetime.now)
    

# model for doctor
class Doctor(Base):
    __tablename__ = "doctor"

    doctor_id = Column(Integer, primary_key=True, index=True)
    full_name_dr = Column(String)
    department = Column(String)
    specialization = Column(String)
    qualification = Column(String)
    experience = Column(String)
    phone = Column(String)
    email = Column(String)
    room_number = Column(Integer)
    consultation_fee = Column(Integer)
    department = Column(String)
    doctor_status = Column(String, default="Active")

# model for apponitment
from sqlalchemy import Column, Integer, String, DateTime, Time, ForeignKey

class Appontment(Base):
    __tablename__ = "appontment"

    appointment_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey("patient.patient_id"))
    doctor_id = Column(Integer, ForeignKey("doctor.doctor_id"))

    appointment_date = Column(DateTime)
    appointment_time = Column(Time)

    reason_for_visit = Column(String)
    appointment_status = Column(String, default="Scheduled")
    

# model for medical record
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

class MedicalRecord(Base):
    __tablename__ = "medicalrecord"

    medical_record_id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    patient_id = Column(Integer, ForeignKey("patient.patient_id"))
    doctor_id = Column(Integer, ForeignKey("doctor.doctor_id"))
    appointment_id = Column(Integer, ForeignKey("appontment.appointment_id"))

    visit_date = Column(DateTime)
    symptoms = Column(String)
    diagnosis = Column(String)
    prescription = Column(String)
    treatment_notes = Column(String)
    follow_up_date = Column(DateTime)


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String(30), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)