from django import forms
from core.models import Student, Grade, Subject
from django.contrib.auth.models import User


from django import forms
from core.models import Grade, Student, Subject

class GradeCreateForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'subject', 'score', 'date', 'comment']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'score': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
        labels = {
            'student': 'Ученик',
            'subject': 'Предмет',
            'score': 'Оценка',
            'date': 'Дата',
            'comment': 'Комментарий',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ['full_name', 'group', 'birth_date']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ФИО ученика'}),
            'group': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: 10А'}),
        }
        labels = {
            'full_name': 'ФИО ученика',
            'group': 'Класс/Группа',
            'birth_date': 'Дата рождения',
        }


class GradeForm(forms.ModelForm):

    class Meta:
        model = Grade
        fields = ['subject', 'score', 'date', 'comment']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Комментарий учителя'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'score': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'subject': 'Предмет',
            'score': 'Оценка',
            'date': 'Дата оценки',
            'comment': 'Комментарий',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['score'].choices = [
            (5, '5 - Отлично'),
            (4, '4 - Хорошо'),
            (3, '3 - Удовлетворительно'),
            (2, '2 - Неудовлетворительно')
        ]