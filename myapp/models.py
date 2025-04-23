from django.contrib.auth.models import User
from django.db import models
from datetime import date, timedelta
from django.utils import timezone

class UserReg(models.Model):
    fname=models.CharField(max_length=50)
    lname=models.CharField(max_length=50)
    addrs=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    phno=models.CharField(max_length=12)
    uname=models.CharField(max_length=50)
    pswrd=models.CharField(max_length=50)
    highest_qualification = models.CharField(max_length=100, default="Not Specified")
    skills = models.TextField(blank=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    is_blocked = models.BooleanField(default=False)  # New field to track block status

class CompanyReg(models.Model):

    company_name = models.CharField(max_length=50)
    company_email = models.EmailField(unique=True)
    address = models.TextField()
    contact_person = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    website = models.URLField(blank=True, null=True)
    username = models.CharField(max_length=50, )
    password = models.CharField(max_length=50)  # In production, use hashed password
    company_logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)
    rights = models.CharField(max_length=2, default='NC')

class AdminLogin(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)  # Use hashed passwords in real apps

class ContactMessage(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=15, null=True, blank=True) # Updated field name
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Message from {self.name} "


class JobVacancy(models.Model):

    company = models.ForeignKey(CompanyReg, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    location = models.CharField(max_length=50, default=True, help_text="City, State or Remote/Hybrid")
    responsibilities = models.TextField(default=True)
    number_of_vacancies = models.PositiveIntegerField(default=1)
    salary_range = models.CharField(max_length=50,default=True, help_text="e.g., 3-5 LPA or 'Negotiable'")
    work_experience = models.CharField(max_length=50,default=True, help_text="e.g., 0-1 years, 2-3 years, etc.")
    skills_required = models.TextField(help_text="Comma-separated skills")
    qualification_required = models.CharField(
        max_length=50,
        help_text="e.g., B.Tech, BCA, MBA (comma-separated if multiple)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    last_date_to_apply = models.DateField(default=date.today() + timedelta(days=30))
    status = models.CharField(max_length=20, default='Active')

    def is_expired(self):
        return self.last_date_to_apply < timezone.now().date()

    def __str__(self):
        return f"{self.title} at {self.company.company_name}"


class JobApplication(models.Model):

    vacancy = models.ForeignKey(JobVacancy, on_delete=models.CASCADE)
    user = models.ForeignKey(UserReg, on_delete=models.CASCADE)
    fname = models.CharField(max_length=50)
    email = models.EmailField()
    phno = models.CharField(max_length=12)
    addrs = models.CharField(max_length=50)
    skills = models.TextField()
    highest_qualification = models.CharField(max_length=50)
    resume = models.FileField(upload_to='application_resumes/', null=True, blank=True)
    status = models.CharField(max_length=30, default='Applied')  # Applied, Shortlisted, Rejected, Interview Date Fixed
    interview_date = models.DateField(null=True, blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.fname} applied for {self.vacancy.title}"