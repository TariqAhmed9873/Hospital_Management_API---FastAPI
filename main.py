from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models, schemas
from datetime import datetime, timedelta
from sqlalchemy import func

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# home api
@app.get("/home", status_code=status.HTTP_200_OK)
async def home():
    return{
        "Message":"This APIs for Hospital Managment System"
    }

# register API
@app.post("/register", response_model=schemas.UserResponse)
async def registerapi(register: schemas.CreateUser, db: Session = Depends(get_db)):
    regigisted = models.User = (
        username == register.username,
        email == register.email,
        password == register.password,
        role == register.role
    )

    db.add(regigisted)
    db.commit()
    db.refresh(regigisted)

    return regigisted

# login API


# all about dashboard
@app.get("/dashboard")
async def dashboard(db: Session = Depends(get_db)):

    today = datetime.now().date()

    one_month_ago = datetime.now() - timedelta(days=30)

    total_patients = db.query(models.Patient).count()
    total_doctor = db.query(models.Doctor).count()
    todays_appointment = db.query(models.Appontment).filter(func.date(models.Appontment.appointment_date) == today).count()
    complete_appointment = db.query(models.Appontment).filter(models.Appontment.appointment_status == "Completed").count()
    cancell_appointment = db.query(models.Appontment).filter(models.Appontment.appointment_status == "Cancelled").count()
    medical_record = db.query(models.MedicalRecord).count()
    new_patient_this_month = db.query(models.Patient).filter(models.Patient.registration_date >= one_month_ago).count()
    active_doctor = db.query(models.Doctor).filter(models.Doctor.doctor_status == "Active").count()

    return{
        "Total Patients": total_patients,
        "Total Doctor": total_doctor,
        "Today's Appointment": todays_appointment,
        "Completed Appointment": complete_appointment,
        "Cancelled Appointment": cancell_appointment,
        "Total Medical Records": medical_record,
        "New Patients this Month": new_patient_this_month,
        "Active Doctor": active_doctor
    }

# all about dashboard charts
@app.get("/dashboard/charts")
async def dashboard_charts(db: Session = Depends(get_db)):

    # Appointment by Month
    appointments_by_month = (
        db.query(
            func.extract("month", models.Appontment.appointment_date).label("month"),
            func.count(models.Appontment.appointment_id).label("appointments")
        )
        .group_by(func.extract("month", models.Appontment.appointment_date))
        .order_by(func.extract("month", models.Appontment.appointment_date))
        .all()
    )

    appointments_by_month = [
        {
            "month": int(row.month),
            "appointments": row.appointments
        }
        for row in appointments_by_month
    ]

    # Daily Appointments
    daily_appointments = (
        db.query(
            func.date(models.Appontment.appointment_date).label("date"),
            func.count(models.Appontment.appointment_id).label("appointments")
        )
        .group_by(func.date(models.Appontment.appointment_date))
        .order_by(func.date(models.Appontment.appointment_date))
        .all()
    )

    daily_appointments = [
        {
            "date": str(row.date),
            "appointments": row.appointments
        }
        for row in daily_appointments
    ]

    # Patients by Gender
    patients_by_gender = (
        db.query(
            models.Patient.gender,
            func.count(models.Patient.patient_id).label("total")
        )
        .group_by(models.Patient.gender)
        .all()
    )

    patients_by_gender = [
        {
            "gender": row.gender,
            "total": row.total
        }
        for row in patients_by_gender
    ]

    # Patients by Blood Group
    patients_by_blood_group = (
        db.query(
            models.Patient.blood_group,
            func.count(models.Patient.patient_id).label("total")
        )
        .group_by(models.Patient.blood_group)
        .all()
    )

    patients_by_blood_group = [
        {
            "blood_group": row.blood_group,
            "total": row.total
        }
        for row in patients_by_blood_group
    ]

    # Doctors by Department
    doctors_by_department = (
        db.query(
            models.Doctor.department,
            func.count(models.Doctor.doctor_id).label("total")
        )
        .group_by(models.Doctor.department)
        .all()
    )

    doctors_by_department = [
        {
            "department": row.department,
            "total": row.total
        }
        for row in doctors_by_department
    ]

    # Most Visited Doctors
    most_visited_doctors = (
        db.query(
            models.Doctor.full_name_dr,
            func.count(models.Appontment.appointment_id).label("visited")
        )
        .join(
            models.Appontment,
            models.Doctor.doctor_id == models.Appontment.doctor_id
        )
        .group_by(models.Doctor.full_name_dr)
        .order_by(func.count(models.Appontment.appointment_id).desc())
        .limit(10)
        .all()
    )

    most_visited_doctors = [
        {
            "doctor_name": row.full_name_dr,
            "visited": row.visited
        }
        for row in most_visited_doctors
    ]

    # Appointment Status Distribution
    appointment_status_distribution = (
        db.query(
            models.Appontment.appointment_status,
            func.count(models.Appontment.appointment_id).label("total")
        )
        .group_by(models.Appontment.appointment_status)
        .all()
    )

    appointment_status_distribution = [
        {
            "status": row.appointment_status,
            "total": row.total
        }
        for row in appointment_status_distribution
    ]

    # Recently Registered Patients
    recent_patients = (
        db.query(models.Patient)
        .order_by(models.Patient.registration_date.desc())
        .limit(5)
        .all()
    )

    recent_patients = [
        {
            "patient_id": p.patient_id,
            "full_name": p.full_name,
            "gender": p.gender,
            "registration_date": p.registration_date
        }
        for p in recent_patients
    ]

    # Upcoming Appointments
    upcoming_appointment = (
        db.query(models.Appontment)
        .filter(
            models.Appontment.appointment_date >= datetime.now(),
            models.Appontment.appointment_status == "Scheduled"
        )
        .order_by(models.Appontment.appointment_date)
        .limit(5)
        .all()
    )

    upcoming_appointment = [
        {
            "appointment_id": a.appointment_id,
            "patient_id": a.patient_id,
            "doctor_id": a.doctor_id,
            "appointment_date": a.appointment_date,
            "appointment_status": a.appointment_status
        }
        for a in upcoming_appointment
    ]

    # Latest Medical Records
    latest_medical_records = (
        db.query(models.MedicalRecord)
        .order_by(models.MedicalRecord.visit_date.desc())
        .limit(5)
        .all()
    )

    latest_medical_records = [
        {
            "medical_record_id": m.medical_record_id,
            "patient_id": m.patient_id,
            "doctor_id": m.doctor_id,
            "diagnosis": m.diagnosis,
            "visit_date": m.visit_date
        }
        for m in latest_medical_records
    ]

    return {
        "Appointments by Month": appointments_by_month,
        "Daily Appointments": daily_appointments,
        "Patients by Gender": patients_by_gender,
        "Patients by Blood Group": patients_by_blood_group,
        "Doctors by Department": doctors_by_department,
        "Most Visited Doctors": most_visited_doctors,
        "Appointment Status Distribution": appointment_status_distribution,
        "Recently Registered Patients": recent_patients,
        "Upcoming Appointments": upcoming_appointment,
        "Latest Medical Records": latest_medical_records
    }

# All about patient
# add new patient
@app.post("/add_patient", response_model=schemas.ResponcePatient, status_code=status.HTTP_201_CREATED)
async def addpatient(add_patient: schemas.CreatePatient, db: Session = Depends(get_db)):
    patient = models.Patient(
        full_name = add_patient.full_name,
        gender = add_patient.gender,
        date_of_birth = add_patient.date_of_birth,
        blood_group = add_patient.blood_group,
        phone_number = add_patient.phone_number,
        email = add_patient.email,
        address = add_patient.address,
        emergency_contact = add_patient.emergency_contact,
    )

    db.add(patient)
    db.commit()
    db.refresh(patient)

    return patient

# see patient list
@app.get("/see_patient", response_model=list[schemas.ResponcePatient], status_code=status.HTTP_200_OK)
async def seepatient(db: Session = Depends(get_db)):
    return db.query(models.Patient).all()

# see patient by id
@app.get("/see_patient_id/{id}", response_model=schemas.ResponcePatient, status_code=status.HTTP_200_OK)
async def seepatient_id(id: int, db: Session = Depends(get_db)):
    patient_id = db.query(models.Patient).filter(models.Patient.patient_id == id).first()

    if not patient_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient Not Found"
        )

    db.commit()
    db.refresh(patient_id)

    return patient_id

# search patient by Name
@app.get("/search_patient_name/{name}", response_model=schemas.ResponcePatient, status_code=status.HTTP_200_OK)
async def searchpatient_name(name: str, db: Session = Depends(get_db)):
    patient_name = db.query(models.Patient).filter(models.Patient.full_name == name).first()

    if not patient_name:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient Not Found"
        )

    db.commit()
    db.refresh(patient_name)

    return patient_name

# update patient by id
@app.put("/update_patient/{id}", response_model=schemas.ResponcePatient, status_code=status.HTTP_200_OK)
async def updatepatient(id: int, update_patient: schemas.ResponcePatient, db: Session = Depends(get_db)):
    update = db.query(models.Patient).filter(models.Patient.patient_id == id).first()

    if not update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient Not Found"
        )

    update.full_name = update_patient.full_name,
    update.gender = update_patient.gender,
    update.date_of_birth = update_patient.date_of_birth,
    update.blood_group = update_patient.blood_group,
    update.phone_number = update_patient.phone_number,
    update.email = update_patient.email,
    update.address = update_patient.address,
    update.emergency_contact = update_patient.emergency_contact,
    update.registration_date = update_patient.registration_date

    db.commit()
    db.refresh(update)

    return update

# delete patient by id
@app.delete("/delete_patient/{id}")
async def deletepatient(id: int, db: Session = Depends(get_db)):
    delete_patient = db.query(models.Patient).filter(models.Patient.patient_id == id).first()

    if not delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient Not Found"
        )

    db.delete(delete_patient)
    db.commit()

    return{
        "Message":"Patient Delete Successfully"
    }

# All about Doctor
# add doctor
@app.post("/add_doctor", response_model=schemas.ResponceDoctor, status_code=status.HTTP_201_CREATED)
async def adddoctor(add_doctor: schemas.CreateDoctor, db: Session = Depends(get_db)):
    doctor = models.Doctor(
        full_name_dr = add_doctor.full_name_dr,
        department = add_doctor.department,
        specialization = add_doctor.specialization,
        qualification = add_doctor.qualification,
        experience = add_doctor.experience,
        phone = add_doctor.phone,
        email = add_doctor.email,
        room_number = add_doctor.room_number,
        consultation_fee = add_doctor.consultation_fee
    )

    db.add(doctor)
    db.commit()
    db.refresh(doctor)

    return doctor

# see doctor by list
@app.get("/see_doctor", response_model=list[schemas.ResponceDoctor])
async def seedoctor(db: Session = Depends(get_db)):
    return db.query(models.Doctor).all()

# see doctor by id
@app.get("/see_doctor_id/{doctor_id}", response_model=schemas.ResponceDoctor)
async def seedoctor_id(doctor_id : int, db: Session = Depends(get_db)):
    doctorid = db.query(models.Doctor).filter(models.Doctor.doctor_id == doctor_id).first()

    if not doctorid:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found"
        )
    
    db.commit()
    db.refresh(doctorid)

    return doctorid

# see doctor by name
@app.get("/see_doctor_name/{doctor_name}", response_model=schemas.ResponceDoctor)
async def see_docorname(doctor_name: str, db: Session = Depends(get_db)):
    doctorname = db.query(models.Doctor).filter(models.Doctor.full_name_dr == doctor_name).first()

    if not doctorname:
        raise HTTPException(
            status_code=status.HTTP_201_CREATED,
            detail="Doctor Not Found"
        )
    
    db.commit()
    db.refresh(doctorname)

    return doctorname

# see doctor by specialization
@app.get("/see_docto_specialization/{specialization}", response_model=schemas.ResponceDoctor)
async def see_specialization(specialization: str, db: Session = Depends(get_db)):
    dr_specialization = db.query(models.Doctor).filter(models.Doctor.specialization == specialization).first()

    if not dr_specialization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor Not Found"
        )
    
    db.commit()
    db.refresh(dr_specialization)

    return dr_specialization

# see doctor by Department
@app.get("/see_docto_department/{department}", response_model=schemas.ResponceDoctor, status_code=status.HTTP_201_CREATED)
async def see_specialization(department: str, db: Session = Depends(get_db)):
    dr_deparment = db.query(models.Doctor).filter(models.Doctor.department == department).first()


    if not dr_deparment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor Not Found"
        )
    
    db.commit()
    db.refresh(dr_deparment)

    return dr_deparment

# update doctor record
@app.put("/update_doctor/{dr_id}", response_model=schemas.ResponceDoctor, status_code=status.HTTP_201_CREATED)
async def updatedoc(dr_id: int, update_doctor: schemas.ResponceDoctor, db: Session = Depends(get_db)):
    dr_update = db.query(models.Doctor).filter(models.Doctor.doctor_id == dr_id).first()

    if not dr_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor Not Found"
        )
    
    dr_update.full_name_dr = update_doctor.full_name_dr,
    dr_update.department = update_doctor.department,
    dr_update.specialization = update_doctor.specialization,
    dr_update.qualification = update_doctor.qualification,
    dr_update.experience = update_doctor.experience,
    dr_update.phone = update_doctor.phone,
    dr_update.email = update_doctor.email,
    dr_update.room_number = update_doctor.room_number,
    dr_update.consultation_fee = update_doctor.consultation_fee

    db.commit()
    db.refresh(dr_update)

    return dr_update

# delete doctor
@app.delete("/delete_doctor/{dr_id}")
async def deletedr(dr_id: int, db: Session = Depends(get_db)):
    delete_dr = db.query(models.Doctor).filter(models.Doctor.doctor_id == dr_id).first()

    if not delete_dr:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found"
        )
    
    db.delete(delete_dr)

    return{
        "Message":"Doctor Delete Successfully"
    }

# All about appointment
# add apointment --> Book Appointment
@app.post("/add_appointment", response_model=schemas.ResponceAppontment, status_code=status.HTTP_201_CREATED)
async def addappointment(add_appointment: schemas.CreateAppontment, db: Session = Depends(get_db)):
    appointment = models.Appontment(
        patient_id = add_appointment.patient_id,
        doctor_id = add_appointment.doctor_id,
        appointment_date = add_appointment.appointment_date,
        appointment_time = add_appointment.appointment_time,
        reason_for_visit = add_appointment.reason_for_visit,
        appointment_status = add_appointment.appointment_status
    )

    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    return appointment

# view all addappointment
@app.get("/view_appointment", response_model=list[schemas.ResponceAppontment], status_code=status.HTTP_200_OK)
async def viewappointment(db: Session = Depends(get_db)):
    return db.query(models.Appontment).all()

# View Appointment by ID
@app.get("/view_appoinment_id/{appointment_id}", response_model=schemas.ResponceAppontment, status_code=status.HTTP_200_OK)
async def appointmentid(appointment_id: int, db: Session = Depends(get_db)):
    vappointment_id = db.query(models.Appontment).filter(models.Appontment.appointment_id == appointment_id).first()

    if not vappointment_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    
    db.commit()
    db.refresh(vappointment_id)

    return vappointment_id

# View Patient Appointments
@app.get("/view_patient_appointment/{patient_id}", response_model=schemas.ResponceAppontment, status_code=status.HTTP_200_OK)
async def patientappointment_id(patient_id: int, db: Session = Depends(get_db)):
    patientappointmentid = db.query(models.Appontment).filter(models.Appontment.patient_id == patient_id).first()

    if not patientappointmentid:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found on this id"
        )
    
    db.commit()
    db.refresh(patientappointmentid)

    return patientappointmentid

# View Doctor Appointments
@app.get("/doctor_appointment/{dr_id}", response_model=schemas.ResponceAppontment, status_code=status.HTTP_200_OK)
async def dr_appointmentid(dr_id: int, db: Session = Depends(get_db)):
    dr_appointment_id = db.query(models.Appontment).filter(models.Appontment.doctor_id == dr_id).first()

    if not dr_appointment_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor's Appointment Not Found"
        )
    
    db.commit()
    db.refresh(dr_appointment_id)

    return dr_appointment_id

# View Today's Appointments
@app.get("/todays_appointment{appointment_date}", response_model=schemas.ResponceAppontment, status_code=status.HTTP_200_OK)
async def todayappointment(appointment_date: int, db: Session = Depends(get_db)):
    today_appointments = db.query(models.Appontment).filter(models.Appontment.appointment_date == appointment_date).first()

    if not today_appointments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    
    db.commit()
    db.refresh(today_appointments)

    return today_appointments

# Update Appointment
@app.put("/update_appointment/{appointment_id}", response_model=schemas.ResponceAppontment, status_code=status.HTTP_200_OK)
async def update_appoint(appointment_id: int, update_appointment: schemas.ResponceAppontment, db: Session = Depends(get_db)):
    update_appointments = db.query(models.Appontment).filter(models.Appontment.appointment_id == appointment_id).first()

    if not update_appointments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    
    update_appointments.patient_id = update_appointment.patient_id,
    update_appointments.doctor_id = update_appointment.doctor_id,
    update_appointments.appointment_date = update_appointment.appointment_date,
    update_appointments.appointment_time = update_appointment.appointment_time,
    update_appointments.reason_for_visit = update_appointment.reason_for_visit,
    update_appointments.appointment_status = update_appointment.appointment_status

    db.commit()
    db.refresh(update_appointments)

    return update_appointments

# Cancel Appointment
@app.put("/clancell_status/{appointment_id}")
async def cancellappointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment_stat = db.query(models.Appontment).filter(models.Appontment.appointment_id == appointment_id).first()

    if not appointment_stat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appoinment not found"
        )
    
    if appointment_stat.appointment_status == "Cancelled":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Appointment already cancelled"
        )
    
    if appointment_stat.appointment_status == "Completed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Appointment completed not cancelled yet"
        )
    
    appointment_stat.appointment_status = "Cancelled"

    db.commit()
    db.refresh(appointment_stat)

    return appointment_stat

# Delete Appointment
@app.delete("/delete_appointment/{appointment_id}")
async def delete(appointment_id: int, db: Session = Depends(get_db)):
    delete_appointment = db.query(models.Appontment).filter(models.Appontment.appointment_id == appointment_id).first()

    if not delete_appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    
    db.delete(delete_appointment)
    db.commit()
    
    return{
        "Message":"Appointment delete successfully"
    }

#all about medical report
#create medical report
@app.post("/create_medical_report", response_model=schemas.ResponceMedicalRecord, status_code=status.HTTP_201_CREATED)
async def createreport(medical_report: schemas.CreateMedicalRecord, db: Session = Depends(get_db)):
    create_report = models.MedicalRecord(
        patient_id = medical_report.patient_id,
        doctor_id = medical_report.doctor_id,
        appointment_id = medical_report.appointment_id,
        visit_date = medical_report.visit_date,
        symptoms = medical_report.symptoms,
        diagnosis = medical_report.diagnosis,
        prescription = medical_report.prescription,
        treatment_notes = medical_report.treatment_notes,
        follow_up_date = medical_report.follow_up_date
    )

    db.add(create_report)
    db.commit()
    db.refresh(create_report)

    return create_report

# view all medical records
@app.get("/view_all_medical_report", response_model=list[schemas.ResponceMedicalRecord], status_code=status.HTTP_201_CREATED)
async def medicalreport(db: Session = Depends(get_db)):
    return db.query(models.MedicalRecord).all()

#view medical record by id
@app.get("/medical_report_id/{medical_id}", response_model=schemas.ResponceMedicalRecord, status_code=status.HTTP_201_CREATED)
async def medicalreport_id(medical_id: int, db: Session = Depends(get_db)):
    medical_report = db.query(models.MedicalRecord).filter(models.MedicalRecord.medical_record_id == medical_id).first()

    if not medical_report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medical Record not found"
        )
    
    db.commit()
    db.refresh(medical_report)

    return medical_report

#View Patient Medical History
@app.get("/patient_medical/{patient_medical_id}", response_model=schemas.ResponceMedicalRecord, status_code=status.HTTP_201_CREATED)
async def patientmedical(patient_medical_id: int, db: Session = Depends(get_db)):
    patient_medi_id = db.query(models.MedicalRecord).filter(models.MedicalRecord.medical_record_id == patient_medical_id).first()

    if not patient_medi_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient Medical Record Not Found"
        )
    
    db.commit()
    db.refresh(patient_medi_id)

    return patient_medi_id

# Update Medical Record
@app.put("/update_medical_report/{medical_patient_id}", response_model=schemas.ResponceMedicalRecord, status_code=status.HTTP_201_CREATED)
async def updatemedical(medical_patient_id: int, update_medical_report: schemas.ResponceAppontment, db: Session = Depends(get_db)):
    medical_pat_id = db.query(models.MedicalRecord).filter(models.MedicalRecord.medical_record_id == medical_patient_id).first()

    if not medical_pat_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medical Record not Found"
        )
    
    medical_pat_id.doctor_id = update_medical_report.doctor_id,
    medical_pat_id.appointment_id = update_medical_report.appointment_id,
    medical_pat_id.visit_date = update_medical_report.visit_date,
    medical_pat_id.symptoms = update_medical_report.symptoms,
    medical_pat_id.diagnosis = update_medical_report.diagnosis,
    medical_pat_id.prescription = update_medical_report.prescription,
    medical_pat_id.treatment_notes = update_medical_report.treatment_notes,
    medical_pat_id.follow_up_date = update_medical_report.follow_up_date

    db.commit()
    db.refresh(medical_pat_id)

    return medical_pat_id

# Delete Medical Record
@app.delete("/delete_medical/{medical_id}")
async def deletemedical_record(medical_id: int, db: Session = Depends(get_db)):
    medical_reocord_id = db.query(models.MedicalRecord).filter(models.MedicalRecord.medical_record_id == medical_id).first()

    if not medical_reocord_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medical Record Not Found"
        )
    
    db.delete(medical_reocord_id)

    return{
        "Message":"Patient Medical Record Delete Successfully"
    }