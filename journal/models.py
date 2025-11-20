from django.db import models
from django.contrib.auth.models import User  # Добавьте этот импорт
from django.conf import settings

# Create your models here.

class Group(models.Model):
    name = models.CharField("Название группы", max_length=50)
    course = models.IntegerField("Курс", null=True, blank=True)  # Добавьте эту строку

    def __str__(self):
        if self.course:
            return f"{self.name} ({self.course} курс)"
        else:
            return self.name

    def student_count(self): 
        return self.student_set.count()

class Student(models.Model):
    name = models.CharField("ФИО студента", max_length=100)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="Группа")
    birth_date = models.DateField("Дата рождения", null=True, blank=True)
    user_profile = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.group.name})"
    
class Teacher(models.Model):
    user_profile = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Студент")
    date = models.DateField("Дата занятия")
    present = models.BooleanField("Присутствовал", default=True)

    class Meta:
        unique_together = ('student', 'date')  # Исправлены кавычки

    def __str__(self):
        status = "Присутствовал" if self.present else "Отсутствовал"
        return f"{self.student.name} - {self.date}: {status}"