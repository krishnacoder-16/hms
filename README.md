# 🏥 Mini Hospital Management System (HMS)

## 📸 Project Preview

### Doctor Dashboard – Manage Availability
![Doctor Dashboard](assets/Doctor_Dashboard.png)
![Doctor Add Slot](assets/Doctor_add_slot.png)

### Patient Booking – Available Slots
![Patient Dashboard](assets/Patient_dashboard.png)

### Appointment Confirmation
![Appointment Confirmation](assets/patient_appointment.png)

A full-stack Mini Hospital Management System designed to simulate real-world healthcare scheduling. The system allows doctors to manage availability, patients to book appointments, and automatically sends email notifications and Google Calendar events for confirmed bookings.

This project demonstrates backend architecture, database design, API integrations, and serverless microservices.

## 🚀 Features

### ✅ Level 1 – Core System
* Secure Doctor and Patient Authentication
* Role-based dashboards
* PostgreSQL database integration
* Clean and responsive UI using Bootstrap

**Doctor Capabilities**
* Create availability time slots
* View and manage personal schedules
* Prevent duplicate or past slots

**Patient Capabilities**
* View registered doctors
* See real-time available slots
* Book appointments instantly

### ✅ Level 2 – Appointment Booking Logic
* Real-time slot availability check
* Prevents double booking
* Automatically marks slots as booked
* Stores appointment records in database
* Displays patient appointment history

### ✅ Level 3 – Serverless Email Notifications
* Implemented using AWS Lambda + Serverless Framework
* Sends emails for:
  * User Signup Welcome
  * Booking Confirmation
* Runs locally with `serverless-offline`
* Communicates with Django backend via HTTP API

### ✅ Level 4 – Google Calendar Integration
* Automatically creates events when appointments are booked
* Events include:
  * Doctor name
  * Patient name
  * Appointment date and time
* Invitations sent to both doctor and patient calendars

---

## 🧠 Key Design Decisions

**Microservice Architecture**  
The email system runs as a separate serverless service, keeping the main application lightweight.

**Secure Credential Handling**  
Sensitive credentials such as:
* `.env`
* `credentials.json`
* `token.json`  
are excluded from Git using `.gitignore`.

**Reliable Booking Logic**  
Slots are validated at the backend to prevent race conditions and double booking.

**Clean Modular Structure**  
Each major functionality is separated into Django apps:
* `accounts`
* `doctors`
* `bookings`

---

## 📂 Project Structure

```text
mini-hospital-management-system/
│
├── bookings/                 # Appointment booking logic
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── doctors/                  # Doctor availability system
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   └── urls.py
│
├── accounts/                 # Authentication & roles
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── email-service/            # Serverless email notification microservice
│   ├── handler.py
│   ├── serverless.yml
│   ├── requirements.txt
│   └── package.json
│
├── hms_project/              # Django project configuration
│   ├── settings.py
│   ├── urls.py
│   └── calendar_service.py   # Google Calendar integration
│
├── templates/                # HTML templates
│
├── venv/                     # Python virtual environment
├── manage.py
├── .env
├── .gitignore
└── README.md
```

---

## 🛠️ Technologies Used

**Backend**
* Django
* Python
* Django ORM

**Database**
* PostgreSQL

**Frontend**
* HTML5
* Bootstrap
* Django Templates

**APIs & Integrations**
* Google Calendar API
* SMTP Email (Gmail)

**Serverless**
* AWS Lambda
* Serverless Framework
* serverless-offline

**Tools**
* Requests (API communication)
* Google Auth Libraries

---

## 🧪 How to Run the Project

### 1️⃣ Clone the Repository
```bash
git clone <repository-url>
cd mini-hospital-management-system
```

### 2️⃣ Setup Virtual Environment
```bash
python -m venv venv
```
**Activate:**
* Windows:
  ```bash
  venv\Scripts\activate
  ```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables
Create `.env` file in the root directory:
```env
SECRET_KEY=your_secret_key
DATABASE_URL=postgres://postgres:password@localhost:5432/hms_db
DEBUG=True
```

### 5️⃣ Setup PostgreSQL Database
Create the database:
```sql
CREATE DATABASE hms_db;
```
Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6️⃣ Run Django Server
```bash
python manage.py runserver
```
Open your browser and navigate to: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 📧 Running the Email Service

Navigate to the serverless service directory:
```bash
cd email-service
```
Install dependencies:
```bash
npm install
```
Start serverless locally:
```bash
serverless offline
```
The email API will run at: `http://localhost:3000/dev/email/send`

---

## 📅 Google Calendar Setup

1. Create a Google Cloud Project
2. Enable Google Calendar API
3. Download `credentials.json`
4. Place it inside the root directory (alongside `manage.py`).

On the first run, authentication will generate a `token.json` file.

---

## 🎥 Demo Features

The demo showcases:
* Doctor signup and login
* Doctor creates availability slots
* Patient views doctors and slots
* Patient books appointment
* Booking confirmation email
* Google Calendar event creation

---

## 🤖 AI Assistance Disclaimer

AI tools were used for learning, debugging, and architectural guidance, including:
* Designing serverless email architecture
* Debugging Django routing and database integration
* Understanding OAuth and Google Calendar API setup

All code was implemented, tested, and refined manually to ensure correct functionality and best practices.

---

## 👨‍💻 Author

**Krishna Kumar**  
B.Tech Computer Science Engineering  
JIMS Greater Noida
