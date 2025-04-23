from django.contrib.admin.views.decorators import staff_member_required
import logging
from datetime import datetime, date
import pyttsx3

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.http import HttpResponse

from django.db.models import Max, Value, F
from django.db.models.functions import Coalesce

from reportlab.pdfgen import canvas

from myapp.models import (
    UserReg,
    CompanyReg,
    AdminLogin,
    ContactMessage,
    JobVacancy,
    JobApplication,
)

logger = logging.getLogger(__name__)


# Create your views here.


def index(request):
    jobs = JobVacancy.objects.all().order_by('-created_at')[:3]  # Adjust field as needed
    return render(request,'index.html',{'jobs':jobs})

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')


def adminhome(request):
    return render(request,'adminhome.html')

def userpage(request):
    jobs = JobVacancy.objects.all().order_by('-created_at')[:3]  # Adjust field as needed
    total_vacancy_count = JobVacancy.objects.count()
    return render(request, 'userpage.html', {
        'jobs': jobs,
        'total_vacancy_count': total_vacancy_count
    })


def companypage(request):
    return render(request, 'companypage.html')

def logout(request):
    return redirect("/index")

def userreg(request):
    if request.method == "POST":
        fstname = request.POST.get('first-name')
        lstname = request.POST.get('last-name')
        addres = request.POST.get('address')
        emailid = request.POST.get('your-email')
        phno = request.POST.get('phno')
        usrname = request.POST.get('uname')
        psword = request.POST.get('password')
        qualification = request.POST.get('qualification')
        skills = request.POST.get('skills')
        resume = request.FILES.get('resume')
        ur = UserReg(fname=fstname, lname=lstname, addrs=addres, email=emailid, phno=phno, uname=usrname, pswrd=psword,highest_qualification=qualification,
            skills=skills,resume=resume)
        ur.save()
        msg = "Hello " + fstname + " " + lstname + " Registration Completed Successfully!"
        return render(request, 'success.html', {"msg": msg, "registration_success": True})
    return render(request, "ureg.html")

def recreg(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        contact_person = request.POST.get('contact-person')
        phno = request.POST.get('phno')
        website = request.POST.get('website')
        uname = request.POST.get('uname')
        password = request.POST.get('password')
        logo = request.FILES.get('company-logo')  # if you later add logo upload field

        cr = CompanyReg(company_name=name,company_email=email,address=address,contact_person=contact_person,phone_number=phno,
            website=website,username=uname,password=password,company_logo=logo  # optional
        )
        cr.save()

        msg = "Hello " + name  + " Registration Complete,Subject to Admin Approval!"

        return render(request, 'success.html', {"msg": msg, "registration_success": True})

    return render(request,'recreg.html')

def login(request):
    if request.method == "POST":
        u = request.POST.get("username")
        p = request.POST.get("password")
        found = 0
        uname = ""
        rights = ""
        company_name = ""
        id = None

        # User login check
        mrec = UserReg.objects.filter(uname=u, pswrd=p)
        if mrec.exists():
            user = mrec.first()
            if user.is_blocked:
                msg = "Your account is blocked. Please contact the admin."

                # 🔊 Voice feedback
                engine = pyttsx3.init()
                engine.say(msg)
                engine.runAndWait()

                return render(request, "login.html", {"msg": msg})
            else:
                found = 1
                id = user.id
                uname = user.fname
                rights = "user"

        # Company login check
        if found == 0:
            crec = CompanyReg.objects.filter(username=u, password=p)
            if crec.exists():
                for j in crec:
                    if j.rights == "AC":  # Approved Company
                        found = 1
                        id = j.id
                        uname = j.company_name
                        rights = "AC"

                        # ✅ Set session variables for company
                        request.session['user_type'] = 'company'
                        request.session['company_id'] = j.id
                        request.session['company_name'] = j.company_name

                          # or whatever your company home page is

                    elif j.rights == "NC":  # New Company
                        msg = "Your company registration is pending admin approval."

                        engine = pyttsx3.init()
                        engine.say(msg)
                        engine.runAndWait()

                        return render(request, "login.html", {"msg": msg})

                    elif j.rights == "RJ":  # Rejected Company
                        msg = "Your company registration has been rejected. Please contact the admin."

                        engine = pyttsx3.init()
                        engine.say(msg)
                        engine.runAndWait()

                        return render(request, "login.html", {"msg": msg})

        # Admin login check
        if found == 0:
            arec = AdminLogin.objects.filter(username=u, password=p)
            if arec.exists():
                found = 1
                for a in arec:
                    id = a.id
                    uname = u
                    rights = "admin"

        # If user found, set session and redirect
        if found == 1:
            request.session['id'] = id
            request.session['user_type'] = 'user'
            request.session['uname'] = uname
            request.session['username'] = u
            request.session['password'] = p
            request.session['rights'] = rights

            # Set company session only if it's a company login
            if rights == "AC" and isinstance(j, CompanyReg):
                request.session['cid'] = j.id
                request.session['cname'] = j.company_name

            if rights == "admin":
                return redirect('/adminhome/')
            elif rights == "user":
                return redirect('/userpage/')
            elif rights == "AC":
                return redirect('/companypage/')
        else:
            msg = "Sorry, wrong Username or Password. Please try again."
            return render(request, "login.html", {"msg": msg})

    return render(request, "login.html")

def user_profile(request):
    user_id = request.session.get('id')
    try:
        user = UserReg.objects.get(id=user_id)
    except UserReg.DoesNotExist:
        return redirect('login')

    if request.method == "POST":
        user.fname = request.POST.get('fname')
        user.lname = request.POST.get('lname')
        user.addrs = request.POST.get('addrs')
        user.email = request.POST.get('email')
        user.phno = request.POST.get('phno')
        user.highest_qualification = request.POST.get('qualification')
        raw_skills = request.POST.get('skills', '')
        cleaned_skills = ",".join([s.strip() for s in raw_skills.split(',') if s.strip()])
        user.skills = cleaned_skills

        if request.FILES.get('resume'):
            user.resume = request.FILES.get('resume')

        user.save()
        msg = "Profile updated successfully!"
        return render(request, 'user_profile.html', {'user': user, 'msg': msg})

    return render(request, 'user_profile.html', {'user': user})

def admin_home(request):
    if request.session.get('rights') != 'admin':
        return redirect('/login/')  # Optional access control

    user_count = UserReg.objects.count()
    approved_company_count = CompanyReg.objects.filter(rights='AC').count()
    total_company_count = CompanyReg.objects.count()
    total_vacancy_count = JobVacancy.objects.filter(status='Active').count()
    query_count = ContactMessage.objects.count()

    return render(request, 'adminhome.html', {
        'user_count': user_count,
        'approved_company_count': approved_company_count,
        'total_company_count': total_company_count,
        'total_vacancy_count': total_vacancy_count,
        'query_count': query_count,
    })

def company_profile(request):
    company_id = request.session.get('id')
    try:
        company = CompanyReg.objects.get(id=company_id)
    except CompanyReg.DoesNotExist:
        return redirect('login')

    if request.method == "POST":
        company.company_name = request.POST.get('company_name')
        company.company_email = request.POST.get('company_email')
        company.address = request.POST.get('address')
        company.contact_person = request.POST.get('contact_person')
        company.phone_number = request.POST.get('phone_number')
        company.website = request.POST.get('website')

        if request.FILES.get('company_logo'):
            company.company_logo = request.FILES.get('company_logo')

        company.save()
        msg = "Company profile updated successfully!"
        return render(request, 'company_profile.html', {'company': company, 'msg': msg})

    return render(request, 'company_profile.html', {'company': company})

def changepassword(request):
    if request.method == "POST":
        oldpass = request.POST.get("old")
        newpass = request.POST.get("n1")
        confrmpass = request.POST.get("n2")

        # Retrieve user session data
        u = request.session.get('username')
        p = request.session.get('password')

        if u is None or p is None:  # If session variables are missing
            msg = "Session expired. Please log in again."
            return render(request, 'change_pass.html', {"msg": msg})

        if p == oldpass:
            if newpass == confrmpass:
                if request.session.get('rights') == 'user':  # User password change
                    updated_rows = UserReg.objects.filter(uname=u, pswrd=p).update(pswrd=newpass)
                    if updated_rows > 0:
                        msg = f"Password Changed Successfully! Please Login Again"
                        return render(request, 'change_pass.html', {"msg": msg})
                    else:
                        msg = "Error: User not found or password not updated. Please try again."
                        return render(request, 'change_pass.html', {"msg": msg})
                else:  # Company password change
                    updated_rows = CompanyReg.objects.filter(username=u, password=p).update(password=newpass)
                    if updated_rows > 0:
                        msg = f"Password Changed Successfully! Please Login Again"
                        return render(request, 'change_pass.html', {"msg": msg})
                    else:
                        msg = "Error: Company not found or password not updated. Please try again."
                        return render(request, 'change_pass.html', {"msg": msg})
            else:
                msg = "Sorry, the new passwords do not match. Please try again."
                return render(request, 'change_pass.html', {"msg": msg})
        else:
            msg = "Sorry, the old password is incorrect. Please try again."
            return render(request, 'change_pass.html', {"msg": msg})

    return render(request, "change_pass.html")


def contact_view(request):
    msg = ""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile_number = request.POST.get('mobile_number')
        message = request.POST.get('message')

        try:
            ContactMessage.objects.create(
                name=name,
                email=email,
                mobile_number=mobile_number,
                message=message
            )
            msg = "Your message has been sent successfully! Admin will contact you shortly."
        except Exception as e:
            msg = "Sorry, there was an error sending your message. Please try again."

        return render(request, 'contact.html', {'msg': msg})

    return render(request, 'contact.html', {'msg': msg})

def admin_queries_view(request):
    messages = ContactMessage.objects.all().order_by('-created_at')
    return render(request, 'admin_queries.html', {'messages': messages})

@staff_member_required
def mark_as_read_view(request, msg_id):
    msg = get_object_or_404(ContactMessage, id=msg_id)
    msg.is_read = True
    msg.save()
    return redirect('admin_queries')

@staff_member_required
def delete_message_view(request, msg_id):
    msg = get_object_or_404(ContactMessage, id=msg_id)
    msg.delete()
    return redirect('admin_queries')

def pending_companies(request):
    if request.session.get('rights') != 'admin':
        return redirect('/login/')

    pending = CompanyReg.objects.filter(rights='NC')
    return render(request, 'pending_companies.html', {'pending_companies': pending})

def approve_company(request, company_id):
    if request.session.get('rights') != 'admin':
        return redirect('/login/')

    company = get_object_or_404(CompanyReg, id=company_id)
    company.rights = 'AC'
    company.save()
    return redirect('pending_companies')  # Redirect back to pending list

def reject_company(request, company_id):
    if request.session.get('rights') != 'admin':
        return redirect('/login/')

    company = get_object_or_404(CompanyReg, id=company_id)
    company.rights = 'RJ'  # Mark as rejected
    company.save()
    return redirect('pending_companies')

def all_companies(request):
    if request.session.get('rights') != 'admin':
        return redirect('/login/')

    companies = CompanyReg.objects.all().order_by('-id')  # latest first
    return render(request, 'all_companies.html', {'companies': companies})

def all_users(request):
    if request.session.get('rights') != 'admin':
        return redirect('/login/')

    users = UserReg.objects.all()
    return render(request, 'all_users.html', {'users': users})

def block_user(request, user_id):
    user = get_object_or_404(UserReg, id=user_id)
    user.is_blocked = True
    user.save()
    return redirect('all_users')

def unblock_user(request, user_id):
    user = get_object_or_404(UserReg, id=user_id)
    user.is_blocked = False
    user.save()
    return redirect('all_users')

def delete_users(request):
    if request.session.get('rights') != 'admin':
        return redirect('login')
    users = UserReg.objects.all()
    return render(request, 'delete_users.html', {'users': users})

def delete_user(request, user_id):
    if request.session.get('rights') != 'admin':
        return redirect('login')
    user = get_object_or_404(UserReg, id=user_id)
    user.delete()
    return redirect('delete_users')


def add_vacancy(request):
    logger.debug(f"Session data: {request.session.items()}")

    # Ensure company is logged in with proper rights

    # Get the company object
    try:
        company = CompanyReg.objects.get(id=request.session['cid'])
    except CompanyReg.DoesNotExist:
        logger.debug("Company not found, redirecting to login")
        messages.error(request, "Company not found. Please log in again.")
        return redirect('/login/')

    if request.method == "POST":
        last_date_str = request.POST.get('last_date_to_apply')
        last_date_to_apply = datetime.strptime(last_date_str, '%Y-%m-%d').date()
        # Get form data
        form_data = {
            'title': request.POST.get('title'),
            'description': request.POST.get('description'),
            'location': request.POST.get('location'),
            'responsibilities': request.POST.get('responsibilities'),
            'number_of_vacancies': request.POST.get('number_of_vacancies'),
            'salary_range': request.POST.get('salary_range'),
            'work_experience': request.POST.get('work_experience'),
            'skills_required': request.POST.getlist('skills_required'),
            'qualification_required': request.POST.get('qualification_required'),
            'last_date_to_apply': last_date_to_apply,  # ✅ New field added here
        }

        # Check if any field is empty
        if not all(form_data.values()):
            messages.error(request, "All fields are required.")
            return render(request, 'add_vacancy.html')

        try:
            # Create job vacancy
            JobVacancy.objects.create(
                company=company,
                title=form_data['title'],
                description=form_data['description'],
                location=form_data['location'],
                responsibilities=form_data['responsibilities'],
                number_of_vacancies=int(form_data['number_of_vacancies']),
                salary_range=form_data['salary_range'],
                work_experience=form_data['work_experience'],
                skills_required=','.join(form_data['skills_required']),
                qualification_required=form_data['qualification_required'],
                last_date_to_apply=form_data['last_date_to_apply'],
            )
            messages.success(request, f"Job vacancy '{form_data['title']}' posted successfully.")

            # Optional: Voice feedback
            try:
                engine = pyttsx3.init()
                engine.say(f"Job vacancy {form_data['title']} posted successfully.")
                engine.runAndWait()
            except Exception as e:
                logger.error(f"Voice feedback error: {str(e)}")

            return redirect('/company_add_vacancy')

        except ValueError as e:
            logger.error(f"ValueError: {str(e)}")
            messages.error(request, "Invalid input. Please check the number of vacancies.")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            messages.error(request, "An error occurred. Please try again.")

        return render(request, 'add_vacancy.html')

    # Handle GET request
    logger.debug("Rendering add_vacancy.html for GET request")
    return render(request, 'add_vacancy.html')


def view_jobs(request):
    logger.debug(f"Session data: {request.session.items()}")
    user = None
    applied_jobs = []
    if request.session.get('rights') == 'user':
        try:
            user = UserReg.objects.get(id=request.session['id'])
            applied_jobs = JobApplication.objects.filter(user=user).values_list('vacancy__id', flat=True)
        except UserReg.DoesNotExist:
            logger.debug("User not found in view_jobs")
            return redirect('/login/')

    today = timezone.now().date()
    jobs = JobVacancy.objects.filter(status='Active',last_date_to_apply__gte=today)
    return render(request, 'view_jobs.html', {
        'jobs': jobs,
        'applied_jobs': applied_jobs,
        'user': user
    })


def apply_for_job(request, job_id):
    logger.debug(f"Session data: {request.session.items()}")
    if request.session.get('rights') != 'user':
        logger.debug("Redirecting to login: rights != 'user'")
        return redirect('/login/')

    try:
        user = UserReg.objects.get(id=request.session['id'])
        if user.is_blocked:
            msg = "Your account is blocked. Please contact the admin."
            engine = pyttsx3.init()
            engine.say(msg)
            engine.runAndWait()
            return render(request, "login.html", {"msg": msg})

        vacancy = get_object_or_404(JobVacancy, id=job_id)

        # Check if user has already applied
        if JobApplication.objects.filter(user=user, vacancy=vacancy).exists():
            msg = f"You have already applied for {vacancy.title}."
            return render(request, "view_jobs.html", {
                "jobs": JobVacancy.objects.all(),
                "msg": msg
            })

        # Create new application
        JobApplication.objects.create(
            vacancy=vacancy,
            user=user,
            fname=user.fname,
            email=user.email,
            phno=user.phno,
            addrs=user.addrs,
            skills=user.skills,
            highest_qualification=user.highest_qualification,
            resume=user.resume
        )
        msg = f"Application for {vacancy.title} submitted successfully."
        engine = pyttsx3.init()
        engine.say(msg)
        engine.runAndWait()
        return render(request, "userpage.html", {
            "jobs": JobVacancy.objects.all(),
            "msg": msg
        })

    except UserReg.DoesNotExist:
        logger.debug("User not found, redirecting to login")
        return redirect('/login/')
    except JobVacancy.DoesNotExist:
        logger.debug(f"Job vacancy {job_id} not found")
        return redirect('view_jobs')

def view_applications(request):
    logger.debug(f"Session data: {request.session.items()}")


    company = CompanyReg.objects.get(id=request.session['company_id'])
    applications = JobApplication.objects.filter(vacancy__company=company).order_by('-applied_at')

    return render(request, 'view_applications.html', {'applications': applications})

def update_application_status(request, app_id, action):
    application = get_object_or_404(JobApplication, id=app_id)

    if action == 'shortlist':
        application.status = 'Shortlisted'
    elif action == 'reject':
        application.status = 'Rejected'
    elif action == 'appoint':
        application.status = 'Appointed'

    application.save()
    return redirect( '/company_applications' )

# View to fix interview date
def fix_interview_date(request, app_id):
    application = get_object_or_404(JobApplication, id=app_id)
    if request.method == 'POST':
        date_str = request.POST.get('interview_date')
        interview_date = parse_date(date_str)
        if interview_date:
            application.interview_date = interview_date
            application.status = 'Interview Date Fixed'
            application.save()
            return redirect('/company_applications')
    return render(request, 'fix_interview_date.html', {'application': application})

def company_applications(request):
    applications = JobApplication.objects.all()
    return render(request, 'company_applications.html', {'applications': applications})

# For users
def user_applications(request):
    # Check if user is logged in via session
    if request.session.get('user_type') != 'user' or request.session.get('rights') != 'user':
        logger.info(f"No valid user session. Session data: {request.session.items()}")
        return redirect('login')

    # Log session details for debugging
    username = request.session.get('username')
    logger.info(f"Session user: {username}, Rights: {request.session.get('rights')}")

    try:
        # Fetch the UserReg object based on session uname
        user = UserReg.objects.get(uname=username)

        # Fetch job applications for the user
        user_apps = JobApplication.objects.filter(user=user)
        logger.info(f"Found {user_apps.count()} applications for user {username}")
    except UserReg.DoesNotExist:
        logger.error(f"User {username} not found in UserReg model")
        # Clear session to force re-login
        request.session.flush()
        return redirect('login')
    except Exception as e:
        logger.error(f"Error fetching applications for user {username}: {str(e)}")
        user_apps = []  # Fallback to empty list

    # Render the template with user applications
    return render(request, 'view_application_status.html', {'user_applications': user_apps})

def all_job_listings(request):
    if request.session.get('rights') != 'admin':
        return redirect('/login/')

    jobs = JobVacancy.objects.select_related('company').order_by('-created_at')
    return render(request, 'all_job_listings.html', {'jobs': jobs})

def appoint_reject_candidates(request):
    if 'company_id' in request.session:  # assuming you store company ID in session
        company_id = request.session['company_id']
        applications = JobApplication.objects.filter(
            status='Interview Date Fixed',
            vacancy__company_id=company_id  # make sure job has ForeignKey to company
        )
        return render(request, 'appoint_reject.html', {'applications': applications})
    else:
        return redirect('/login')

def company_view_vacancies(request):
    if request.session.get('rights') != 'AC':
        return redirect('/login/')

    company = get_object_or_404(CompanyReg, id=request.session['id'])
    vacancies = JobVacancy.objects.filter(company=company)

    today = timezone.now().date()
    return render(request, 'company_view_vacancies.html', {
        'vacancies': vacancies,
        'today': today
    })

def delete_vacancy(request, vacancy_id):
    vacancy = get_object_or_404(JobVacancy, id=vacancy_id)
    if request.method == 'POST':
        vacancy.status = 'Deleted'
        vacancy.save()
    return redirect('company_view_vacancies')

def admin_view_all_applications(request):
    applications = JobApplication.objects.select_related('vacancy').all()
    return render(request, 'admin_all_applications.html', {'applications': applications})

def approved_companies_list(request):
    companies = CompanyReg.objects.filter(rights='AC')  # Only approved companies
    return render(request, 'companies_list.html', {'companies': companies})

def delete_company(request, company_id):
    if request.method == 'POST':
        company = get_object_or_404(CompanyReg, id=company_id)
        company.delete()
    return redirect('all_companies')

def delete_job(request, job_id):
    job = get_object_or_404(JobVacancy, id=job_id)

    # Soft delete: change status to 'Deleted'
    job.status = 'Deleted'
    job.save()
    messages.success(request, "Job deleted successfully.")
    return redirect('admin_job_listings')

def vacancy_count(request):
    job_vacancy = JobVacancy.objects.filter(status='Active').count() # Or use a filter if needed
    return render(request, 'userpage.html', {
        'total_vacancy_count': job_vacancy,
    })
