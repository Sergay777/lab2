from django.shortcuts import render, redirect  # Добавлен redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from .forms import AttendanceForm

# Create your views here.

def index(request):
    context = {
        'welcome': "Добро пожаловать, уважаемый пользователь!",
        'menu': [
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
@login_required
@user_passes_test(lambda u: u.is_teacher)
def add_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('journal_index')
    else:
        form = AttendanceForm()
    return render(request, 'journal/add_attendance.html', {'form': form})
@login_required
def profile(request):
    if request.user.is_teacher:
        return redirect('home')
    student = getattr(request.user, 'student', None)
    return render(request, 'journal/profile.html', {'student': student})
