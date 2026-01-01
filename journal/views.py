from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from .forms import AttendanceForm
from django.db.models import Count, Q
<<<<<<< Updated upstream
<<<<<<< Updated upstream
from .models import Student, Group, Attendance
=======
=======
>>>>>>> Stashed changes
from .models import Student, Group, Attendance, Lesson, Subject, Teacher, Period, Type_lesson, Att_Status

# ===== Импорты для CBV =====
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView, DetailView
from django.shortcuts import get_object_or_404
from .mixins import TeacherRequiredMixin, StudentRequiredMixin

# ===== ФУНКЦИОНАЛЬНЫЕ ПРЕДСТАВЛЕНИЯ (старые) =====
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes

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

<<<<<<< Updated upstream
<<<<<<< Updated upstream
# === НОВОЕ ПРЕДСТАВЛЕНИЕ: моя посещаемость для студентов ===
@login_required
def my_attendance(request):
    if not request.user.is_student:
        return redirect('home')  # если не студент — на главную

    student = getattr(request.user, 'student', None)
    if not student:
        return render(request, 'journal/my_attendance.html', {'attendance_list': []})

    # Получаем все записи посещаемости для этого студента
    attendance_list = student.attendance_set.all().order_by('-date')
    return render(request, 'journal/my_attendance.html', {'attendance_list': attendance_list})

# === НОВОЕ ПРЕДСТАВЛЕНИЕ: статистика по группам ===
=======
=======
>>>>>>> Stashed changes
@login_required
def my_attendance(request):
    if not request.user.is_student:
        return redirect('home')
    student = getattr(request.user, 'student', None)
    if not student:
        return render(request, 'journal/my_attendance.html', {'attendance_list': []})
    attendance_list = student.attendance_set.all().order_by('-date')
    return render(request, 'journal/my_attendance.html', {'attendance_list': attendance_list})

<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
@login_required
def group_stats(request):
    stats = Group.objects.annotate(
        student_count=Count('student', distinct=True),
        present_count=Count('student__attendance', filter=Q(student__attendance__present=True))
    )
    return render(request, 'journal/group_stats.html', {'stats': stats})

# ===== КЛАССЫ-ПРЕДСТАВЛЕНИЯ ДЛЯ ПРЕПОДАВАТЕЛЯ (Lab 3) =====

class GroupListView(LoginRequiredMixin, TeacherRequiredMixin, ListView):
    model = Group
    template_name = "teacher/groups.html"
    context_object_name = "groups"
    paginate_by = 10

    def get_queryset(self):
        return Group.objects.all().order_by("name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Список учебных групп"
        return context

class StudentListView(LoginRequiredMixin, TeacherRequiredMixin, ListView):
    model = Student
    template_name = "teacher/group_students.html"
    context_object_name = "students"
    paginate_by = 10

    def get_queryset(self):
        group_id = self.kwargs.get("group_id")
        self.group = get_object_or_404(Group, pk=group_id)
        return Student.objects.filter(id_group=self.group).select_related("user").order_by("last_name", "first_name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["group"] = self.group
        context["title"] = f"Студенты группы {self.group.name}"
        return context

class LessonListView(LoginRequiredMixin, TeacherRequiredMixin, ListView):
    model = Lesson
    template_name = "teacher/lessons.html"
    context_object_name = "lessons"
    paginate_by = 10

    def get_queryset(self):
        group_id = self.kwargs.get("group_id")
        if group_id:
            self.group = get_object_or_404(Group, pk=group_id)
            return Lesson.objects.filter(id_group=self.group).select_related("id_subject", "id_teacher", "type", "period").order_by("-date")
        else:
            # Если группа не указана, показываем все занятия преподавателя
            return Lesson.objects.filter(id_teacher=self.request.user.teacher).select_related("id_group", "id_subject", "type", "period").order_by("-date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group = getattr(self, "group", None)
        if group:
            context["group"] = group
            context["title"] = f"Занятия группы {group.name}"
        else:
            context["title"] = "Мои занятия"
        return context

class AttendanceListView(LoginRequiredMixin, TeacherRequiredMixin, ListView):
    model = Attendance
    template_name = "teacher/lesson_attendance.html"
    context_object_name = "attendances"
    paginate_by = 30

    def get_queryset(self):
        lesson_id = self.kwargs.get("lesson_id")
        self.lesson = get_object_or_404(Lesson, pk=lesson_id)
        return Attendance.objects.filter(id_lesson=self.lesson).select_related("id_student__user", "status").order_by("id_student__last_name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lesson"] = self.lesson
        context["group"] = self.lesson.id_group
        context["title"] = f"Посещаемость: {self.lesson.id_subject.name}, {self.lesson.date}"
        return context

# ===== КЛАССЫ-ПРЕДСТАВЛЕНИЯ ДЛЯ СТУДЕНТА (Lab 3) =====

class ProfileView(LoginRequiredMixin, StudentRequiredMixin, TemplateView):
    template_name = "student/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.request.user.student
        context["student"] = student
        context["title"] = "Мой профиль"
        return context

class MyAttendanceView(LoginRequiredMixin, StudentRequiredMixin, ListView):
    model = Attendance
    template_name = "student/my_attendance.html"
    context_object_name = "attendances"
    paginate_by = 15

    def get_queryset(self):
        student = self.request.user.student
        return Attendance.objects.filter(id_student=student).select_related("id_lesson__id_subject", "id_lesson__id_teacher__user", "status").order_by("-id_lesson__date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Моя посещаемость"
        return context