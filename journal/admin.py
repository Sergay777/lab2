from django.contrib import admin
from .models import Group, Student, Attendance, Teacher

# Inline для студентов
class StudentInline(admin.TabularInline):
    model = Student
    extra = 1

class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'group')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'group__name')
    list_filter = ('group',)

class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    inlines = [StudentInline]  # <-- добавляем inline

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'date', 'present')
    list_display_links = ('id', 'student')
    list_filter = ('present', 'student__group', 'date')
    search_fields = ('student__name',)
    ordering = ('-date',)

admin.site.register(Teacher)
admin.site.register(Student, StudentAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Attendance, AttendanceAdmin)