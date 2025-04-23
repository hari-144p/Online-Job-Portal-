Online Job Portal using Python Django
Overview
This Python-based Online Job Portal, developed using the Django web framework, serves as a dynamic platform that seamlessly connects job seekers with companies offering diverse employment opportunities. The portal facilitates an end-to-end recruitment process, enabling companies to register, post job vacancies, and manage applications, while job seekers can create profiles, apply for jobs, and track application statuses.
Features

User & Company Registration: Separate registration and login systems for job seekers and companies, with admin approval required for companies.
Company Dashboard:
Post job vacancies with specific skill sets and qualifications.
View and manage posted jobs.
Review applications and take actions (Shortlist or Reject).
Schedule interviews for shortlisted candidates.


Job Application System: Users can browse job listings, apply with auto-submitted profiles, and upload resumes.
Application Tracking System: Companies can view applicants per job, with shortlisted applications managed on a dedicated "Interview Fixing" page. Status updates (e.g., Shortlisted, Interview Scheduled) are visible to users.
Interview Scheduling: Companies can set interview dates/times for shortlisted applicants, with status updates reflected in user dashboards.
User Dashboard: View applied jobs, track statuses, and receive updates for shortlisting or interview calls.
Admin Controls: Manage company approvals and oversee platform operations.

Technology Used

Programming Language: Python
Libraries/Frameworks:
Django (backend framework)
Bootstrap (frontend styling)


Database: SQLite (easily replaceable with PostgreSQL or MySQL)
Authentication: Django Auth (separate roles for Employee and Employer)
Frontend: HTML, CSS, Bootstrap
Development Environment: VS Code, PyCharm, or similar IDEs

Installation

Clone the repository:git clone https://github.com/yourusername/job-portal-project.git


Navigate to the project directory:cd job-portal-project


Create and activate a virtual environment:python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install dependencies:pip install -r requirements.txt


Run database migrations:python manage.py makemigrations
python manage.py migrate


Create a superuser (for admin panel access):python manage.py createsuperuser


Run the development server:python manage.py runserver


Open your browser and go to:http://127.0.0.1:8000/



Usage
For Job Seekers:

Register and create a profile.
Browse job listings and apply with your profile and resume.
Track application statuses (e.g., Shortlisted, Interview Scheduled) via the user dashboard.

For Companies:

Register and await admin approval.
Post job vacancies with required skills and qualifications.
Review applications, shortlist candidates, and schedule interviews.
Manage all job postings and applicant statuses via the company dashboard.

For Admins:

Log in to the admin panel (/admin).
Approve company registrations and oversee platform activities.

Project Structure
job-portal-project/
├── job_portal/            # Main Django project folder
├── company/               # Company-specific features
├── users/                 # User authentication and profile handling
├── media/                 # Uploaded files (e.g., resumes)
├── templates/             # HTML templates
├── static/                # Static CSS/JS
├── requirements.txt       # Python dependencies
├── manage.py
└── README.md

Screenshots
(You can add screenshots here of registration, job posting, application tracking, etc.)
License
This project is open-source and available under the MIT License.
Contact

Name: Harigovind S
BCA 3rd Year
Stream: Computer Application
College: Mar Augusthinose College
Email: harigovind940@gmail.com

