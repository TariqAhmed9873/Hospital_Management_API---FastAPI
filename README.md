# 🏥 Hospital Management System API

A backend **Hospital Management System REST API** built with **Python, FastAPI, SQLAlchemy, and PostgreSQL**.

This project provides APIs for managing patients, doctors, appointments, medical records, authentication, and hospital dashboard statistics.

---

## 🚀 Features

* 🔐 User Registration & Login
* 🔑 JWT Authentication
* 👤 Current User Profile
* 🔒 Change Password
* 🧑‍⚕️ Patient Management
* 👨‍⚕️ Doctor Management
* 📅 Appointment Management
* 🏥 Medical Record Management
* 📊 Hospital Dashboard
* 🗄️ PostgreSQL Database
* 🔗 SQLAlchemy ORM
* ✅ Business Rules & Validation

---

## 🛠️ Technologies Used

| Technology        | Purpose                   |
| ----------------- | ------------------------- |
| Python            | Backend Programming       |
| FastAPI           | REST API Framework        |
| SQLAlchemy        | ORM / Database Operations |
| PostgreSQL        | Database                  |
| Pydantic          | Data Validation           |
| JWT               | Authentication            |
| Uvicorn           | API Server                |
| Postman / Swagger | API Testing               |

---

## 📁 Project Structure

```text
Hospital Management System/
│
├── main.py
├── database.py
├── models.py
├── schemas.py
├── auth.py
├── .env
├── requirements.txt
└── README.md
```

> **Note:** This project does not use a `routers/` folder. The API endpoints are implemented directly in `main.py`.

---

# 🗄️ Database

The project uses **PostgreSQL**.

### Database Name

```text
hospital_db
```

### Main Tables

```text
users
patients
doctors
appointments
medical_records
```

---

# 🔐 Authentication APIs

### Register User

```http
POST /register
```

Creates a new user account.

### Login

```http
POST /login
```

Authenticates the user and returns a JWT access token.

### Current User

```http
GET /me
```

Returns the currently authenticated user's information.

### Change Password

```http
PUT /change_password
```

Allows an authenticated user to change their password.

---

# 🧑‍⚕️ Patient APIs

### Add Patient

```http
POST /add_patient
```

### Get All Patients

```http
GET /see_patient
```

### Get Patient by ID

```http
GET /see_patient_id/{patient_id}
```

### Update Patient

```http
PUT /update_patient/{patient_id}
```

### Delete Patient

```http
DELETE /delete_patient/{patient_id}
```

---

# 👨‍⚕️ Doctor APIs

### Add Doctor

```http
POST /add_doctor
```

### Get All Doctors

```http
GET /see_doctor
```

### Get Doctor by ID

```http
GET /see_doctor_id/{doctor_id}
```

### Update Doctor

```http
PUT /update_doctor/{doctor_id}
```

### Delete Doctor

```http
DELETE /delete_doctor/{doctor_id}
```

---

# 📅 Appointment APIs

### Book Appointment

```http
POST /book_appointment
```

### Get All Appointments

```http
GET /see_appointment
```

### Get Appointment by ID

```http
GET /see_appointment/{appointment_id}
```

### Update Appointment

```http
PUT /update_appointment/{appointment_id}
```

### Cancel Appointment

```http
PUT /cancel_appointment/{appointment_id}
```

### Delete Appointment

```http
DELETE /delete_appointment/{appointment_id}
```

---

# 🏥 Medical Record APIs

### Create Medical Record

```http
POST /create_medical_record
```

### Get All Medical Records

```http
GET /see_medical_records
```

### Get Medical Record by ID

```http
GET /see_medical_record/{record_id}
```

### Update Medical Record

```http
PUT /update_medical_record/{record_id}
```

### Delete Medical Record

```http
DELETE /delete_medical_record/{record_id}
```

---

# 📊 Dashboard API

```http
GET /dashboard
```

The dashboard provides hospital statistics such as:

* Total Patients
* Total Doctors
* Today's Appointments
* Completed Appointments
* Cancelled Appointments
* Total Medical Records
* New Patients
* Active Doctors

---

# 📋 Business Rules

The system follows important hospital management rules:

1. A patient must exist before booking an appointment.
2. A doctor must exist before booking an appointment.
3. A doctor cannot have two appointments at the same date and time.
4. Medical records can only be created for completed appointments.
5. Cancelled appointments cannot have medical records.
6. Each medical record is connected to one appointment.
7. Cancelled appointments are kept in the database.
8. Completed appointments should not be deleted; their status is maintained.

---

# 🔑 Authentication Flow

```text
Register
   ↓
Login
   ↓
JWT Access Token
   ↓
Authorization Header
   ↓
Protected API
```

Example:

```http
Authorization: Bearer <access_token>
```

---

# ▶️ How to Run

### 1. Clone the Repository

```bash
git clone <your-github-repository-url>
```

### 2. Open Project

```bash
cd Hospital-Management-System
```

### 3. Create Virtual Environment

```bash
python -m venv venv
```

### 4. Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure Database

Create your PostgreSQL database:

```text
hospital_db
```

Configure your database connection in the project environment/configuration.

### 7. Start FastAPI Server

```bash
uvicorn main:app --reload
```

---

# 📖 API Documentation

After starting the server, open:

### Swagger UI

```text
http://127.0.0.1:8000/docs
```

Swagger can be used to test all API endpoints.

---

# 🧪 API Testing

The APIs can be tested using:

* FastAPI Swagger UI
* Postman

Recommended testing flow:

```text
Register User
      ↓
Login
      ↓
Get JWT Token
      ↓
Add Doctor
      ↓
Add Patient
      ↓
Book Appointment
      ↓
Complete Appointment
      ↓
Create Medical Record
      ↓
View Dashboard
```

---

# 📌 Project Purpose

The purpose of this project is to demonstrate a complete backend system for hospital management using modern Python backend technologies.

It demonstrates:

* REST API development
* Authentication
* CRUD operations
* Database relationships
* Data validation
* Business logic
* PostgreSQL integration
* SQLAlchemy ORM
* API documentation
* Dashboard statistics

---

# 👨‍💻 Author

**Tariq Ahmed**

BSCS Student | Python & FastAPI Backend Developer | Cloud Engineering | AI & LLM Engineering

---
