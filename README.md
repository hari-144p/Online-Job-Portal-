🧑‍💼 Job Portal Project

A web-based job portal built using Python and Django that connects job seekers with companies offering employment opportunities.

🚀 Features

👥 User & Company Registration

Separate registration and login system for job seekers and companies.

Companies require admin approval before accessing features (New Company -> Approved Company).

🏢 Company Dashboard

Post new job vacancies with required skill sets and qualifications.

View and manage all posted jobs.

View job applications and take action (Shortlist or Reject).

Schedule interviews for shortlisted candidates.

📄 Job Application System

Users can browse job listings and apply.

Application includes auto-submitted profile details and uploaded resume.

📋 Application Tracking System

Companies can view applicants per job posting.

Shortlisted applications appear in a dedicated 'Interview Fixing' page.

Status updates visible to users: 'Shortlisted', 'Interview Scheduled', etc.

📆 Interview Scheduling

Companies can set an interview date/time for each shortlisted applicant.

Status updates reflected in user dashboard.

🧑‍💼 User Dashboard

View applied jobs and their current status.

Receive updates when shortlisted or called for interview.

🛠️ Tech Stack

Backend: Django (Python)

Frontend: HTML, CSS, Bootstrap

Database: SQLite (Easy to replace with PostgreSQL or MySQL)

Authentication: Django Auth (Separate roles for Employee & Employer)

🔧 Setup Instructions

Clone the repository:

git clone https://github.com/yourusername/job-portal-project.git
cd job-portal-project

Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Run database migrations:

python manage.py makemigrations
python manage.py migrate

Create a superuser (for admin panel access):

python manage.py createsuperuser

Run the development server:

python manage.py runserver

Open your browser and go to:

http://127.0.0.1:8000/

📁 Project Structure (Sample)

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

📸 Screenshots

(You can add screenshots here of registration, job posting, application tracking, etc.)

📝 License

This project is licensed under the MIT License.

🙋‍♂️ Author

Harigovind S
