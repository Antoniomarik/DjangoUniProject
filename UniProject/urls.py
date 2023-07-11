"""
URL configuration for UniProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from project import views
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views
from UniProject import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")), 
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('accounts/profile', views.check_logged_in_user, name='check_logged_in_user'),
    path('check-logged-in-user/', views.check_logged_in_user, name='check_logged_in_user'),

    path('adminpage/', views.admin_page, name='adminpage'),
    path('professorpage/', views.professor_page, name='professorpage'),
    path('studentpage/', views.student_page, name='studentpage'),

    path('logout/', auth_views.LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='auth_logout'),

    path('professors/', views.professors, name='professors'),
    path('subjects/', views.subjects, name='subjects'),
    path('students/', views.students, name='students'),

    path('addprofessor/', views.add_professor, name='add_professor'),
    path('addsubject/', views.add_subject, name='add_subject'),
    path('addstudents/', views.add_student, name='add_student'),

    path('opredmetu/<int:subjectId>', views.subject_details, name='subjectDetails'),
    path('editsubject/<int:subjectId>', views.edit_subjects, name='edit_subject'),
    path('editstudent/<int:studentId>', views.edit_students, name='edit_student'),
    path('editprofesor/<int:profId>', views.edit_profesor, name='edit_profesor'),

    path('upisnilist/<int:studentID>', views.upisni_list, name='upisni_list'),
    path('listapredmeta/', views.professor_subjects, name='listapredmeta'),


    path("obrana/", views.obrana, name="obrana"),
    path("obrana2/<int:pk>", views.obranazad2, name="obranadetalji")
]
