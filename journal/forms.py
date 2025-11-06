from django import forms
from django.core.exceptions import ValidationError
from .models import Attendance

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'date', 'present']
    
    def clean(self):
        cleaned_data = super().clean()
        student = cleaned_data.get('student')
        date = cleaned_data.get('date')
        
        # Проверяем, что оба поля заполнены
        if student and date:
            # Ищем существующие записи для этого студента и даты
            existing_attendance = Attendance.objects.filter(
                student=student, 
                date=date
            )
            
            # Если форма редактирует существующую запись, исключаем её из проверки
            if self.instance and self.instance.pk:
                existing_attendance = existing_attendance.exclude(pk=self.instance.pk)
            
            # Если нашли дубликат, вызываем ошибку валидации
            if existing_attendance.exists():
                raise ValidationError(
                    f"Запись посещаемости для студента {student} на дату {date} уже существует."
                )
        
        return cleaned_data