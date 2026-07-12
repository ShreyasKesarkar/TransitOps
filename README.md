# 🚛 TransitOps

**TransitOps** is a modern Transport Operations Management System developed for the **Odoo Hackathon 2026**. It streamlines fleet operations by enabling organizations to efficiently manage vehicles, drivers, trips, maintenance, fuel consumption, and operational expenses through a centralized web platform.

---

## 🌟 Features

### 🔐 Authentication
- Secure JWT-based Login
- Role-Based Access Control
- Protected Routes

### 🏢 Organization Management
- Organization Registration
- Organization Profile
- Role Management

### 👥 User & Driver Management
- User Management
- Driver Registration
- License Tracking
- Driver Availability
- Safety Score

### 🚛 Fleet Management
- Vehicle Registration
- Vehicle Status Tracking
- Vehicle Types
- Odometer Tracking

### 🗺️ Trip Management
- Create Trips
- Assign Drivers
- Assign Vehicles
- Trip Status Monitoring
- Trip History

### 🔧 Maintenance Management
- Maintenance Requests
- Priority Levels
- Approval Workflow
- Maintenance History

### ⛽ Fuel Management
- Fuel Logs
- Fuel Station Tracking
- Fuel Type
- Odometer Recording
- Fuel Cost Tracking

### 💰 Expense Management
- Operational Expenses
- Expense Categories
- Vehicle-wise Expenses
- Trip-wise Expenses

### 📊 Dashboard & Analytics
- Fleet Overview
- Active Vehicles
- Active Drivers
- Running Trips
- Maintenance Summary
- Fuel & Expense Statistics

---

# 🛠️ Tech Stack

### Frontend
- React
- Vite
- Tailwind CSS
- React Router
- Axios

### Backend
- FastAPI
- SQLAlchemy
- JWT Authentication
- Pydantic

### Database
- PostgreSQL

### Version Control
- Git
- GitHub

---

# 📁 Project Structure

```text
TransitOps/
│
├── frontend/
├── backend/
├── database/
│   └── schema.sql
├── docs/
└── README.md
```

---

# 🗄️ Database Modules

- Organizations
- Roles
- Users
- Drivers
- Vehicle Types
- Vehicles
- Trips
- Maintenance Requests
- Fuel Logs
- Expense Types
- Expenses

---

# 🚀 Getting Started

## Clone Repository

```bash
git clone https://github.com/ShreyasKesarkar/TransitOps.git
```

---

## Backend

```bash
cd backend

pip install -r requirements.txt

uvicorn app.main:app --reload
```

Backend runs on:

```
http://localhost:8000
```

Swagger Documentation:

```
http://localhost:8000/docs
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

Frontend runs on:

```
http://localhost:5173
```

---

## Database

Create a PostgreSQL database named:

```
TranscOps
```

Execute:

```
database/schema.sql
```

---

# 📸 Screenshots

> Screenshots will be added after implementation.

---

# 👥 Team

Developed during **Odoo Hackathon 2026**.

Team Members:

- Shreyas Kesarkar (Team Leader)
- Garima Kriplani
- Manish Tambe
- Shravan shahane

---

# 🎯 Future Scope

- Live GPS Tracking
- Route Optimization
- Notifications
- Reports & Analytics
- Export to Excel/PDF
- Multi-Organization Support
- Mobile Application

---

# 📄 License

This project was developed for the **Odoo Hackathon 2026** for educational and demonstration purposes.
