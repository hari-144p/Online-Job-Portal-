from django.contrib.auth.views import LoginView
from django.urls import path
from .import views
from .views import (
    contact_view,
    admin_queries_view,
    mark_as_read_view,
    delete_message_view
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index,name='index'),
    path('index/',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('login/', views.login, name='login'),
    path('ureg/',views.userreg),
    path('recreg/',views.recreg),
    path('adminhome/',views.admin_home),
    path('logout/', views.logout, name='logout'),
    path('companypage/',views.companypage),
    path('company_profile',views.company_profile),
    path('userpage/',views.userpage),
    path('contact/',views.contact_view),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('change_pass/', views.changepassword, name='change_password'),
    path('admin_queries/', views.admin_queries_view, name='admin_queries'),
    path('admin_queries_read/<int:msg_id>/', views.mark_as_read_view, name='mark_as_read'),
    path('admin_queries_delete/<int:msg_id>/', views.delete_message_view, name='delete_message'),
    path('admin_pending_companies/', views.pending_companies, name='pending_companies'),
    path('admin_approve_company/<int:company_id>/', views.approve_company, name='approve_company'),
    path('admin_reject_company/<int:company_id>/', views.reject_company, name='reject_company'),
    path('admin_companies/', views.all_companies, name='all_companies'),
    path('admin_users/', views.all_users, name='all_users'),
    path('users_block/<int:user_id>/', views.block_user, name='block_user'),
    path('users_unblock/<int:user_id>/', views.unblock_user, name='unblock_user'),
    path('users_delete/', views.delete_users, name='delete_users'),
    path('users_delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('company_add_vacancy/', views.add_vacancy, name='add_vacancy'),
    path('company_applications/', views.view_applications, name='view_applications'),
    path('jobs/', views.view_jobs, name='view_jobs'),
    path('jobs_apply/<int:job_id>/', views.apply_for_job, name='apply_for_job'),
    path('application/<int:app_id>/<str:action>/', views.update_application_status, name='update_application_status'),
    path('fix_interview/<int:app_id>/', views.fix_interview_date, name='fix_interview_date'),
    path('user_applications/', views.user_applications, name='user_applications'),
    path('admin_job_listings/', views.all_job_listings, name='all_job_listings'),
    path('appoint-reject/', views.appoint_reject_candidates, name='appoint_reject_candidates'),
    path('update-status/<int:app_id>/<str:action>/', views.update_application_status, name='update_application_status'),
    path('company_view_vacancies/', views.company_view_vacancies, name='company_view_vacancies'),
    path('company_delete_vacancy/<int:vacancy_id>/', views.delete_vacancy, name='delete_vacancy'),
    path('admin_applications/', views.admin_view_all_applications, name='admin_view_all_applications'),
    path('companies/', views.approved_companies_list, name='approved_companies_list'),
    path('delete_company/<int:company_id>/', views.delete_company, name='delete_company'),
    path('delete_job/<int:job_id>/', views.delete_job, name='delete_job'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)