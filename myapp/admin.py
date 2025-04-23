from django.contrib import admin
from myapp.models import UserReg, CompanyReg, AdminLogin, ContactMessage, JobApplication, JobVacancy

admin.site.register(UserReg)
admin.site.register(CompanyReg)
admin.site.register(AdminLogin)
admin.site.register(ContactMessage)
admin.site.register(JobVacancy)
admin.site.register(JobApplication)

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'mobile_number', 'is_read', 'created_at')  # Updated field
    list_filter = ('is_read', 'created_at')
    actions = ['mark_as_read']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)

