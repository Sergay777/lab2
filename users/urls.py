from django.urls import path
from . import views
urlpatterns = [
 path('register/', views.register, name='register'),
 # (логин/логаут добавим в следующей лабе)
]
