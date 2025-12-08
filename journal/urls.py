from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('about/', views.about, name="about"),
    path('contacts/', views.contacts, name="contacts"),
    path('add/', views.add_attendance, name='attendance_add'),
    path('profile/', views.profile, name='profile'),
    path('teacher/', views.teacher_panel, name='teacher_panel'),
    path('attendance_list/', views.attendance_list, name= 'attendance_list'),
]