# Placement Portal Application

## Overview

A comprehensive **role-based campus placement portal** built with Flask, SQLite, and Bootstrap. Streamlines recruitment activities for institutes, companies, and students with intuitive dashboards, real-time tracking, and efficient approval workflows.

## Features

### 👨‍💼 Admin (Institute Placement Cell)
- Pre-existing admin account with full system control
- Approve/reject company registrations
- Approve/reject placement drives
- View comprehensive system statistics
- Manage and search students by name/contact
- Deactivate or blacklist accounts

### 🏢 Company
- Self-registration with admin approval workflow
- Create, edit, and delete placement drives
- View all student applications
- Shortlist and select candidates
- Track application status and metrics

### 👨‍🎓 Student
- Self-registration and login
- Browse approved placement drives
- Apply for jobs (prevents duplicate applications)
- Track application status in real-time
- View placement history
- Manage profile information

## Tech Stack

| Component | Technology |
|-----------|-------------|
| **Backend** | Flask 2.3.3 |
| **Database** | SQLite |
| **Frontend** | Bootstrap 5, Jinja2 |
| **ORM** | SQLAlchemy |
| **Authentication** | Flask-Login |
| **Forms** | WTForms, Flask-WTF |
| **Python Version** | 3.12+ |

## Project Structure

```
Placement-Portal-Application/
├── app.py                          # Main Flask application entry point
├── models.py                       # SQLAlchemy database models
├── requirements.txt                # Python dependencies
├── placement.db                    # SQLite database (auto-generated)
│
├── routes/                         # Flask Blueprints for modular routing
│   ├── auth_routes.py             # Authentication (login, registration)
│   ├── admin_routes.py            # Admin dashboard and management
│   ├── company_routes.py          # Company operations
│   └── student_routes.py          # Student operations
│
├── templates/                      # Jinja2 HTML templates
│   ├── base.html                  # Base template with navigation
│   ├── index.html, login.html     # Public pages
│   ├── register_company.html      # Company registration
│   ├── register_student.html      # Student registration
│   ├── admin/                     # Admin panel templates
│   ├── company/                   # Company dashboard templates
│   └── student/                   # Student dashboard templates
│
├── static/                        # Static files
│   └── css/style.css             # Custom Bootstrap styling
│
└── PROJECT_REPORT.md             # Detailed project documentation
```

## Quick Start

### Prerequisites
- Python 3.12+
- pip (Python package manager)

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd "https://github.com/24f2009111/Placement-Portal-Application.git"
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   
   # On Windows:
   .\venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Access the application:**
   ```
   Open browser → http://localhost:5000
   ```

## Default Credentials

### Admin Account
- **Username:** `admin`
- **Password:** `admin123`

*Note: Change these credentials in production.*

## User Workflows

### 1. Company Registration & Approval
```
Company registers → Admin reviews → Approval/Rejection → 
Company creates drives → Admin approves drives → 
Drives visible to students
```

### 2. Student Application
```
Student registers → Browse approved drives → 
Apply for drive → Track application status → 
Receive selection/rejection updates
```

### 3. Admin Management
```
Admin dashboard → View statistics → Manage companies/drives/students → 
Search and deactivate accounts
```

## Core Functionalities

✅ **Authentication System**
- Secure login/logout
- Three distinct user roles
- Password hashing with Werkzeug
- Session management with Flask-Login

✅ **Company Management**
- Registration with admin approval
- Full CRUD for placement drives
- Real-time applicant tracking
- Application status updates

✅ **Student Features**
- Browse approved drives only
- Automatic duplicate application prevention
- Application status tracking
- Placement history viewing

✅ **Admin Controls**
- Comprehensive dashboard with KPIs
- Company approval workflow
- Drive management and approval
- Student search and deactivation
- System statistics and reporting

✅ **Data Integrity**
- Proper database constraints
- Role-based access control
- Validation on forms and backend
- SQLite transaction management

## Database Schema

### Tables
- **User:** Core authentication (id, username, email, password, role, is_active)
- **StudentProfile:** Student details and resume
- **CompanyProfile:** Company information and approval status
- **PlacementDrive:** Job postings with eligibility criteria and deadlines
- **Application:** Student applications with status tracking

### Relationships
- User (1) ←→ (1) StudentProfile
- User (1) ←→ (1) CompanyProfile
- CompanyProfile (1) ←→ (M) PlacementDrive
- PlacementDrive (1) ←→ (M) Application
- StudentProfile (1) ←→ (M) Application

## API Routes Summary

### Authentication
- `POST /login` - User login
- `GET/POST /register/company` - Company registration
- `GET/POST /register/student` - Student registration
- `GET /logout` - User logout

### Admin Panel
- `GET /admin/dashboard` - Statistics dashboard
- `GET /admin/companies` - Company management
- `GET /admin/drives` - Drive management
- `GET /admin/students` - Student search

### Company Operations
- `GET /company/dashboard` - Company dashboard
- `POST /company/create-drive` - Create drive
- `GET /company/drive/<id>` - View applications
- `POST /company/update-application-status` - Update status

### Student Portal
- `GET /student/dashboard` - Student dashboard
- `GET /student/available-drives` - Browse drives
- `POST /student/apply/<id>` - Apply for drive
- `GET /student/applications` - View applications
- `GET /student/history` - Placement outcomes

## Validation

The application implements **multi-layer validation:**

1. **Frontend Validation:** HTML5 form constraints
2. **Backend Validation:** 
   - WTForms validators
   - Business logic checks
   - Database constraint enforcement
3. **Duplicate Prevention:** Prevents duplicate applications
4. **Authorization:** Role-based access control on all routes

## Deployment Notes

- Database is created programmatically on first run
- No manual DB setup required
- Admin account auto-created on startup
- All static files served via Flask's static folder
- Debug mode enabled for development (disable in production)

## Testing Checklist

- [x] User registration (company & student)
- [x] Login/logout functionality
- [x] Admin approval workflows
- [x] Drive creation and management
- [x] Student application system
- [x] Status update tracking
- [x] Search functionality
- [x] Role-based access control
- [x] Responsive design on mobile/desktop
- [x] Form validation

## AI/LLM Declaration

**Tool Used:** GitHub Copilot  
**Extent:** ~30% assistance with code structure, templates, CSS  
**Disclaimer:** All core logic, database design, and feature implementation are custom-developed.

## Future Enhancements

- [ ] Email notifications for applications
- [ ] File upload for resumes
- [ ] Advanced analytics and charts
- [ ] REST API endpoints
- [ ] Multiple drive date management
- [ ] Interview scheduling
- [ ] Offer letter generation
- [ ] Alumni tracking

## Troubleshooting

### Database Issues
```bash
# Delete old database and regenerate:
rm placement.db
python app.py
```

### Port Already in Use
```bash
# Run on different port:
python -c "from app import app; app.run(port=5001)"
```

### Module Import Errors
```bash
# Reinstall dependencies:
pip install -r requirements.txt --force-reinstall
```


