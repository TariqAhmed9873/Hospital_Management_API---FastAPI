from pydantic import BaseModel, ConfigDict
from datetime import datetime, time

# for Patient
class CreatePatient(BaseModel):
    full_name : str
    gender : str
    date_of_birth : datetime
    blood_group : str
    phone_number : str
    email : str
    address : str
    emergency_contact : str
    
class ResponcePatient(BaseModel):
    patient_id : int
    full_name : str
    gender : str
    date_of_birth : datetime
    blood_group : str
    phone_number : str
    email : str
    address : str
    emergency_contact : str
    registration_date : datetime
    
    model_config = ConfigDict(from_attributes=True)

# for doctor
class CreateDoctor(BaseModel):
    full_name_dr : str
    department : str
    specialization : str
    qualification : str
    experience : str
    phone : str
    email : str
    room_number : int
    consultation_fee : int
    department : str
    doctor_status : str

class ResponceDoctor(BaseModel):
    doctor_id : int
    full_name_dr : str
    department : str
    specialization : str
    qualification : str
    experience : str
    phone : str
    email : str
    room_number : int
    consultation_fee : int
    department : str
    doctor_status : str

    model_config = ConfigDict(from_attributes=True)

#for appontment
class CreateAppontment(BaseModel):
    patient_id : int
    doctor_id : int
    appointment_date : datetime
    appointment_time : time
    reason_for_visit : str
    appointment_status : str


class ResponceAppontment(BaseModel):
    appointment_id : int
    patient_id : int
    doctor_id : int
    appointment_date : datetime
    appointment_time : time
    reason_for_visit : str
    appointment_status : str


    model_config = ConfigDict(from_attributes=True)

# for medical record
class CreateMedicalRecord(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_id: int
    visit_date: datetime
    symptoms: str
    diagnosis: str
    prescription: str
    treatment_notes: str
    follow_up_date: datetime

class ResponceMedicalRecord(BaseModel):
    medical_record_id: int
    patient_id: int
    doctor_id: int
    appointment_id: int
    visit_date: datetime
    symptoms: str
    diagnosis: str
    prescription: str
    treatment_notes: str
    follow_up_date: datetime

    model_config = ConfigDict(from_attributes=True)

class CreateUser(BaseModel):
    username: str
    email: str
    password: str
    role: str

class UserResponse(BaseModel):
    user_id: int
    username: str
    email: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True

class Login(BaseModel):
    username: str
    password: str