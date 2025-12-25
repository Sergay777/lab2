from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from .forms import AttendanceForm
from django.db.models import Count, Q
from .models import Student, Group, Attendance  # <-- добавь Group и Attendance

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
            return redirect('attendance_add')
    else:
        form = AttendanceForm()
    return render(request, 'journal/add_attendance.html', {'form': form})

@login_required
def profile(request):
    if request.user.is_teacher:
        return redirect('home')
    student = getattr(request.user, 'student', None)
    return render(request, 'journal/profile.html', {'student': student})

@login_required
@user_passes_test(lambda u: u.is_teacher)
def teacher_panel(request):
    return render(request, 'journal/teacher_panel.html')

@login_required
def attendance_list(request):
    return render(request, 'journal/attendance_list.html', {})

@login_required
def attendance_stats(request):
    stats = Student.objects.annotate(
        total=Count('attendance'),
        absences=Count('attendance', filter=Q(attendance__present=False))
    )
    for student in stats:
        if student.total > 0:
            student.attendance_percent = round(((student.total - student.absences) / student.total) * 100, 1)
        else:
            student.attendance_percent = 0
    return render(request, 'journal/stats.html', {'stats': stats})

# === НОВОЕ ПРЕДСТАВЛЕНИЕ: статистика по группам ===
@login_required
def group_stats(request):
    stats = Group.objects.annotate(
        student_count=Count('student', distinct=True),
        present_count=Count('student__attendance', filter=Q(student__attendance__present=True))
    )
    return render(request, 'journal/group_stats.html', {'stats': stats})