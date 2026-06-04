# 🔐 SecureAttend - Blockchain Attendance Management System

<div align="center">

**Enterprise-grade attendance management combining modern web technologies with blockchain integration for secure, transparent, and immutable record-keeping.**

[![GitHub repo](https://img.shields.io/badge/GitHub-SecureAttend-blue?style=flat-square&logo=github)](https://github.com/sreeramakhil/securattend)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-securattend.vercel.app-brightgreen?style=flat-square&logo=vercel)](https://securattend.vercel.app)
[![Python](https://img.shields.io/badge/Python-29.1%25-3776ab?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Solidity](https://img.shields.io/badge/Solidity-4.1%25-363636?style=flat-square&logo=ethereum&logoColor=white)](https://soliditylang.org/)
[![Web3](https://img.shields.io/badge/Web3.js-Smart%20Contracts-F16822?style=flat-square&logo=web3.js&logoColor=white)](https://web3js.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)

**[🎬 Live Demo](https://securattend.vercel.app) • [📖 Documentation](#-documentation) • [🚀 Quick Start](#-quick-start) • [🔗 Smart Contracts](#-smart-contracts)**

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-system-architecture)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [Smart Contracts](#-smart-contracts)
- [API Documentation](#-api-documentation)
- [Deployment](#-deployment)
- [Security Features](#-security-features)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

**SecureAttend** is a production-ready, full-stack attendance management system that reimagines record-keeping through blockchain technology. Unlike traditional attendance systems, SecureAttend provides:

- **Immutable Records**: Every attendance entry is cryptographically secured on the blockchain
- **Transparency**: All records are publicly verifiable and tamper-proof
- **Real-Time Tracking**: Instant attendance updates across all users
- **Enterprise-Scale**: Built to handle institutional and corporate attendance needs
- **Multi-Layer Architecture**: Decoupled frontend, backend, and blockchain layers

### Why SecureAttend?

| Traditional Systems | SecureAttend |
|-------------------|-------------|
| Centralized database (prone to tampering) | Blockchain-backed (immutable) |
| Manual record auditing | Automated smart contract verification |
| Single point of failure | Distributed architecture |
| Limited transparency | Complete audit trail |
| No cryptographic proof | Blockchain-verified authenticity |

**🎬 [Try the Live Demo](https://securattend.vercel.app)**

---

## ✨ Key Features

### 🔐 **Security & Verification**
- **Blockchain Verification**: All attendance records stored on Ethereum/Polygon smart contracts
- **Immutable Records**: Cryptographically secured, tamper-proof attendance logs
- **JWT Authentication**: Secure token-based user authentication
- **Role-Based Access Control**: Admin, Instructor, and User roles with granular permissions
- **Data Encryption**: Sensitive data encrypted at rest and in transit

### 📊 **Attendance Management**
- **Real-Time Recording**: Instant check-in/check-out with timestamp verification
- **Batch Processing**: Bulk attendance operations for large institutions
- **Attendance Verification**: Smart contract validation of attendance authenticity
- **Calendar View**: Visual calendar-based attendance overview
- **Manual Adjustments**: Authorized personnel can modify records with audit trail

### 📈 **Analytics & Reports**
- **Comprehensive Dashboard**: Real-time attendance metrics and KPIs
- **Detailed Reports**: Generate attendance summaries by user, date range, department
- **Trend Analysis**: Visualize attendance patterns and anomalies
- **Export Functionality**: Download reports in CSV/PDF format
- **Statistical Insights**: Attendance rate, absenteeism patterns, peak hours

### 👥 **User Management**
- **Multi-User Support**: Support for students, employees, instructors, admins
- **User Profiles**: Detailed user information and role assignments
- **Bulk Import**: CSV upload for batch user creation
- **Department Management**: Organize users by departments/classes
- **Activity Logs**: Complete audit trail of all user actions

### 🔔 **Notifications & Alerts**
- **Real-Time Notifications**: Instant alerts for attendance events
- **Absence Alerts**: Automatic notifications for unauthorized absences
- **System Alerts**: Dashboard alerts for system events and updates
- **Email Integration**: Optional email notifications for admins

### 📱 **Responsive Interface**
- **Mobile-Friendly UI**: Works seamlessly on desktop, tablet, and mobile
- **Intuitive Dashboard**: Clean, modern interface designed for ease of use
- **Dark Mode Support**: Eye-friendly dark theme option
- **Fast Load Times**: Optimized for speed and performance

---

## 🛠️ Tech Stack

### Frontend Layer (52.5%)
- **HTML5**: Semantic markup and structure
- **CSS3**: Responsive design, animations, styling
- **JavaScript (ES6+)**: Interactive features, DOM manipulation, API calls
- **Fetch API**: RESTful API communication

### Backend Layer (29.1%)
- **Python 3.8+**: Core backend logic
- **Flask/Django**: Web framework for REST APIs
- **SQLAlchemy**: ORM for database management
- **PostgreSQL/SQLite**: Relational database
- **JWT (PyJWT)**: Authentication token management
- **Web3.py**: Blockchain interaction

### Blockchain Layer (4.1%)
- **Solidity 0.8+**: Smart contract development
- **Ethereum/Polygon**: Blockchain network
- **Web3.js**: JavaScript blockchain interactions
- **Truffle/Hardhat**: Smart contract development framework
- **OpenZeppelin Contracts**: Secure smart contract libraries

### Infrastructure & Deployment
- **Vercel**: Frontend hosting and deployment
- **Docker**: Containerization for consistency
- **GitHub Actions**: CI/CD pipeline automation
- **Makefile**: Build automation and task runners

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    SECURATTEND ECOSYSTEM                    │
└─────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────┐
│   Frontend Layer (HTML/CSS/JavaScript)               │
│   • Responsive Dashboard                             │
│   • Real-Time Updates                                │
│   • Web3 Integration                                 │
└────────────────────┬─────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────┐
│   REST API Layer (Python Flask)                      │
│   • Authentication & Authorization                   │
│   • Business Logic                                   │
│   • Data Processing                                  │
└────────────┬──────────────────────────┬──────────────┘
             │                          │
             ▼                          ▼
    ┌────────────────┐          ┌──────────────────┐
    │   SQL Database │          │   Blockchain     │
    │   (PostgreSQL) │          │   Network        │
    └────────────────┘          │ (Ethereum/       │
                                │  Polygon)        │
                                └──────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

```bash
✓ Python 3.8 or higher
✓ Node.js 14+ (for blockchain interaction)
✓ Git
✓ npm or yarn
✓ MetaMask browser extension
```

### Installation

#### Step 1: Clone Repository
```bash
git clone https://github.com/sreeramakhil/securattend.git
cd securattend
```

#### Step 2: Set Up Backend
```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt
```

#### Step 3: Configure Environment
```bash
cp .env.example .env
# Edit .env with your settings
```

#### Step 4: Run Application
```bash
# Terminal 1: Start backend
python app.py

# Terminal 2: Open frontend
cd frontend
python -m http.server 8000
```

**Access**: http://localhost:8000

---

## 📁 Project Structure

```
securattend/
├── frontend/                          # Frontend application
│   ├── index.html                     # Login page
│   ├── dashboard.html                 # Main dashboard
│   ├── admin.html                     # Admin panel
│   ├── reports.html                   # Reports page
│   ├── styles/
│   │   ├── style.css
│   │   ├── dashboard.css
│   │   └── responsive.css
│   ├── scripts/
│   │   ├── app.js
│   │   ├── api.js
│   │   ├── auth.js
│   │   └── web3.js
│   └── assets/
│
├── backend/                           # Backend application
│   ├── app.py                         # Flask app
│   ├── routes/
│   │   ├── auth.py
│   │   ├── attendance.py
│   │   ├── reports.py
│   │   └── admin.py
│   ├── models/
│   │   ├── user.py
│   │   ├── attendance.py
│   │   └── department.py
│   ├── services/
│   │   ├── blockchain_service.py
│   │   ├── attendance_service.py
│   │   └── report_service.py
│   └── requirements.txt
│
├── blockchain/                        # Smart contracts
│   ├── contracts/
│   │   ├── Attendance.sol
│   │   └── AccessControl.sol
│   ├── scripts/
│   │   └── deploy.js
│   ├── test/
│   │   └── Attendance.test.js
│   └── hardhat.config.js
│
├── .env.example
├── Makefile
├── LICENSE
└── README.md
```

---

## 🔗 Smart Contracts

### Core Contract Functions

```solidity
// Record attendance on blockchain
recordAttendance(address _user, uint256 _timestamp, bool _isPresent)

// Verify attendance authenticity
verifyAttendance(address _user, uint256 _timestamp) → bool

// Get attendance history
getAttendanceHistory(address _user) → AttendanceRecord[]

// Get attendance count
getAttendanceCount(address _user, uint256 _start, uint256 _end) → uint256
```

### Deploy Smart Contracts

```bash
cd blockchain
npm install

# Configure your network in hardhat.config.js

# Deploy to Polygon
npx hardhat run scripts/deploy.js --network polygon

# Verify on Etherscan
npx hardhat verify --network polygon CONTRACT_ADDRESS
```

---

## 📚 API Documentation

### Base URL
```
http://localhost:5000/api
```

### Authentication
```
Authorization: Bearer YOUR_JWT_TOKEN
```

### Key Endpoints

#### Register User
```bash
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword",
  "firstName": "John",
  "lastName": "Doe",
  "role": "student"
}
```

#### Login
```bash
POST /api/auth/login
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

#### Record Attendance
```bash
POST /api/attendance/checkin
Authorization: Bearer TOKEN

{
  "userId": "user_123",
  "timestamp": 1718865600000,
  "location": "Building A, Room 101"
}
```

#### Get Attendance Records
```bash
GET /api/attendance?userId=user_123&startDate=2026-06-01&endDate=2026-06-30
Authorization: Bearer TOKEN
```

#### Generate Report
```bash
POST /api/reports/generate
Authorization: Bearer TOKEN

{
  "reportType": "attendance_summary",
  "startDate": "2026-06-01",
  "endDate": "2026-06-30",
  "format": "pdf"
}
```

---

## 🚀 Deployment

### Deploy Frontend to Vercel

```bash
npm install -g vercel
vercel --prod
```

### Deploy Backend to Heroku

```bash
heroku login
heroku create securattend-api
git push heroku main
```

### Docker Deployment

```bash
docker build -t securattend:latest .
docker run -p 5000:5000 securattend:latest
```

---

## 🔐 Security Features

- ✅ **JWT Authentication**: Stateless token-based auth
- ✅ **Role-Based Access Control**: Granular permissions
- ✅ **Password Hashing**: bcrypt with salt
- ✅ **Input Validation**: Sanitized inputs
- ✅ **HTTPS/TLS**: Encrypted data transmission
- ✅ **Rate Limiting**: Prevent brute force attacks
- ✅ **Smart Contract Audits**: Secure contracts
- ✅ **Audit Logging**: Track all actions

---

## 🤝 Contributing

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open Pull Request**

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

---

## 📧 Contact

**Developer**: [Sreeram Akhil](https://github.com/sreeramakhil)

- **GitHub**: [@sreeramakhil](https://github.com/sreeramakhil)
- **Email**: akhilsreeram663@gmail.com
- **Live Demo**: [securattend.vercel.app](https://securattend.vercel.app)

---

<div align="center">

**Made with ❤️ by Sreeram Akhil**

⭐ If you find this project useful, please give it a star!

</div>
