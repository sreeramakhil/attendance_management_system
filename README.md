# Attendance Management System

> A comprehensive full-stack attendance management solution combining modern web technologies with blockchain integration for secure and transparent record-keeping.

[![GitHub repo](https://img.shields.io/badge/GitHub-attendance_management_system-blue?logo=github)](https://github.com/sreeramakhil/attendance_management_system)
[![Live Demo](https://img.shields.io/badge/Live_Demo-securattend.vercel.app-green)](https://securattend.vercel.app)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running Locally](#running-locally)
- [Configuration](#configuration)
- [Usage](#usage)
- [Architecture](#architecture)
- [Smart Contracts](#smart-contracts)
- [Contributing](#contributing)
- [License](#license)
- [Copyright](#copyright)
- [Contact](#contact)

## 🎯 Overview

The **Attendance Management System** is a robust application designed to streamline attendance tracking and management. It leverages a modern full-stack architecture combining:

- **Frontend**: Interactive web interfaces built with HTML, CSS, and JavaScript
- **Backend**: Python-powered REST APIs for business logic and data management
- **Blockchain**: Solidity smart contracts for immutable attendance records

The system is deployed and accessible at [securattend.vercel.app](https://securattend.vercel.app), providing secure, transparent, and efficient attendance management.

## ✨ Features

### Core Functionality
- 📱 **Responsive User Interface** - Clean, intuitive web interface for both administrators and users
- 🔐 **Secure Authentication** - User authentication and authorization mechanisms
- 📊 **Attendance Tracking** - Real-time attendance recording and monitoring
- 📈 **Analytics & Reports** - Comprehensive reporting and data visualization
- 🔗 **Blockchain Integration** - Immutable attendance records on the blockchain
- 📋 **Batch Processing** - Support for bulk attendance operations

### Advanced Features
- ✅ Attendance verification and validation
- 📅 Calendar-based attendance view
- 👥 User and role management
- 🔔 Notifications and alerts
- 📥 Data import/export functionality

## 🛠️ Tech Stack

### Frontend (52.5% - HTML)
- **HTML5** - Semantic markup and structure
- **CSS (9.4%)** - Responsive styling and layout
- **JavaScript (1.9%)** - Interactive frontend logic and DOM manipulation

### Backend (29.1% - Python)
- **Python** - Core backend logic and API development
- **Framework**: Flask/Django (or similar Python web framework)
- **Database**: Integration with relational databases

### Blockchain (4.1% - Solidity)
- **Solidity** - Smart contracts for immutable attendance recording
- **Ethereum/Compatible Chain** - Blockchain network integration

### Build & Deployment
- **Makefile (1.4%)** - Build automation
- **Batchfile (1.6%)** - Windows batch scripts for automation
- **Vercel** - Frontend hosting and deployment

## 📁 Project Structure

```
attendance_management_system/
├── frontend/                  # HTML, CSS, JavaScript files
│   ├── index.html
│   ├── styles/
│   │   └── *.css
│   └── scripts/
│       └── *.js
├── backend/                   # Python backend
│   ├── app.py                # Main application entry
│   ├── routes/               # API endpoints
│   ├── models/               # Data models
│   └── utils/                # Utility functions
├── contracts/                # Solidity smart contracts
│   └── Attendance.sol
├── config/                   # Configuration files
├── Makefile                  # Build automation
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🚀 Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** - For backend development
- **Node.js & npm** - For JavaScript tooling (optional)
- **Git** - For version control
- **Web Browser** - Modern browser (Chrome, Firefox, Safari, Edge)
- **MetaMask** - For blockchain interaction (if using blockchain features)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sreeramakhil/attendance_management_system.git
   cd attendance_management_system
   ```

2. **Set up Python virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install additional dependencies** (if using npm)
   ```bash
   npm install
   ```

### Running Locally

1. **Start the backend server**
   ```bash
   python app.py
   # or
   make run
   ```
   The backend will be available at `http://localhost:5000`

2. **Open the frontend**
   - Navigate to `http://localhost:5000` in your web browser
   - Or open `frontend/index.html` directly if running frontend separately

3. **Access the application**
   - Open [http://localhost:5000](http://localhost:5000)
   - Log in with your credentials

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Flask Configuration
FLASK_ENV=development
FLASK_APP=app.py
SECRET_KEY=your-secret-key-here

# Database Configuration
DATABASE_URL=sqlite:///attendance.db
# or for PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost/attendance_db

# Blockchain Configuration
CONTRACT_ADDRESS=0x...
WEB3_PROVIDER=https://mainnet.infura.io/v3/YOUR-PROJECT-ID
PRIVATE_KEY=your-private-key

# Application Settings
DEBUG=True
LOG_LEVEL=INFO
```

### Database Setup

```bash
# Initialize the database
python -c "from app import db; db.create_all()"

# Or using migration tools
flask db upgrade
```

## 📖 Usage

### For Administrators
1. Log in with admin credentials
2. Navigate to the Admin Dashboard
3. Add users and manage attendance records
4. View analytics and generate reports
5. Configure system settings

### For Users
1. Log in with your credentials
2. View your attendance records
3. Check-in/Check-out if applicable
4. Download attendance reports
5. View attendance history

### API Endpoints

#### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `POST /api/auth/register` - User registration

#### Attendance
- `GET /api/attendance` - Fetch attendance records
- `POST /api/attendance` - Create attendance record
- `GET /api/attendance/:id` - Fetch specific record
- `PUT /api/attendance/:id` - Update attendance record
- `DELETE /api/attendance/:id` - Delete attendance record

#### Reports
- `GET /api/reports` - Generate reports
- `GET /api/reports/summary` - Attendance summary

## 🏗️ Architecture

### System Architecture
```
┌─────────────────────────────────────────┐
│          Frontend Layer                 │
│  (HTML5 | CSS | JavaScript)            │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│          REST API Layer                 │
│  (Python Flask/Django)                 │
└──────────────┬──────────────────────────┘
               │
       ┌───────┴────────┐
       │                │
┌──────▼──────┐   ┌────▼─────────┐
│  Database   │   │  Blockchain  │
│  (SQL)      │   │  (Solidity)  │
└─────────────┘   └──────────────┘
```

## 🔗 Smart Contracts

### Attendance Contract (Solidity)

The smart contract manages immutable attendance records on the blockchain:

- **Record Attendance**: Securely record attendance on-chain
- **Verify Records**: Query and verify attendance history
- **Transparency**: All records are publicly verifiable
- **Immutability**: Records cannot be altered once recorded

Deploy with:
```bash
truffle migrate
# or
hardhat run scripts/deploy.js
```

## 📝 Contributing

Contributions are welcome! Follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is currently unlicensed. See the LICENSE file for more details.

## © Copyright

**Copyright © 2026 Sreeram Akhil. All rights reserved.**

This project and all its contents, including but not limited to:
- Source code
- Documentation
- Images and graphics
- Design and layout
- Smart contracts
- Database schemas
- API specifications

are the intellectual property of **Sreeram Akhil** unless otherwise stated.

### Permitted Uses
- ✅ Viewing and studying the code for educational purposes
- ✅ Forking and modifying for personal use
- ✅ Creating pull requests to contribute improvements
- ✅ Using the application for non-commercial purposes

### Restricted Uses
- ❌ Redistribution without attribution
- ❌ Commercial use without explicit permission
- ❌ Removing or altering copyright notices
- ❌ Claiming ownership of the project or its components
- ❌ Publishing modified versions as your own

### Third-Party Components

This project uses the following open-source libraries and frameworks:
- Python libraries (see `requirements.txt`)
- JavaScript libraries (see `package.json`)
- Solidity libraries (see smart contracts)

Each third-party component is governed by its respective license. Please refer to individual license files for details.

### Disclaimer

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

### Contact for Licensing

For inquiries regarding commercial use, licensing agreements, or other copyright-related matters, please contact:

**Email**: akhilsreeram663@gmail.com  
**GitHub**: [@sreeramakhil](https://github.com/sreeramakhil)

---

## 📧 Contact

**Developer**: [sreeramakhil](https://github.com/sreeramakhil)

- **GitHub**: [@sreeramakhil](https://github.com/sreeramakhil)
- **Email**: akhilsreeram663@gmail.com
- **Live Demo**: [securattend.vercel.app](https://securattend.vercel.app)
- **Repository**: [attendance_management_system](https://github.com/sreeramakhil/attendance_management_system)

---

**Made with ❤️ by [sreeramakhil](https://github.com/sreeramakhil)**

*Last updated: June 2026*
