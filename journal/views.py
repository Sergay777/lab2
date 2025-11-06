from django.shortcuts import render, redirect  # Добавлен redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import AttendanceForm

# Create your views here.

def index(request):
    context = {
        'welcome': "Добро пожаловать, уважаемый пользователь!",
        'menu': [
            {'title': "Главная", 'url_name': 'home'},
            {'title': "О системе", 'url_name': 'about'},
            {'title': "Контакты", 'url_name': 'contacts'}
        ]
    }
    return render(request, 'journal/index.html', context)

def about(request):
    return render(request, 'journal/about.html', {})

def contacts(request):
    return render(request, 'journal/contacts.html', {})

@login_required
def add_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()  # создает новую запись Attendance
            # Можно добавить сообщение успеха, но пока просто редирект
            return redirect('attendance_list')
    else:
        form = AttendanceForm()
    return render(request, 'journal/add_attendance.html', {'form': form})
