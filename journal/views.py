from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from .forms import AttendanceForm

def index(request):
    context = {
        'welcome': "Добро пожаловать, уважаемый пользователь!",
        'menu': []
    }
    return render(request, 'journal/index.html', context)

def about(request):
    return render(request, 'journal/about.html', {})

def contacts(request):
    return render(request, 'journal/contacts.html', {})

@login_required
@user_passes_test(lambda u: u.is_teacher)
def add_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('attendance_add')  # или 'home', если нет 'attendance_list'
    else:
        form = AttendanceForm()
    return render(request, 'journal/add_attendance.html', {'form': form})

@login_required
def profile(request):
    if request.user.is_teacher:
        return redirect('journal/teacher_panel.html')
    student = getattr(request.user, 'student', None)
    return render(request, 'journal/profile.html', {'student': student})

@login_required
@user_passes_test(lambda u: u.is_teacher)
def teacher_panel(request):
    return render(request, 'journal/teacher_panel.html')

@login_required
def attendance_list(request):
    return render(request, 'journal/attendance_list.html',{})