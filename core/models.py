from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    full_name = models.CharField(max_length=200, verbose_name="ФИО")
    group = models.CharField(max_length=50, verbose_name="Класс/Группа")
    birth_date = models.DateField(verbose_name="Дата рождения")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Ученик"
        verbose_name_plural = "Ученики"
        ordering = ['group', 'full_name']

    def __str__(self):
        return f"{self.full_name} ({self.group})"


class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название предмета")

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"

    def __str__(self):
        return self.name


class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Ученик")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Предмет")
    score = models.IntegerField(
        verbose_name="Оценка",
        choices=[(5, '5 - Отлично'), (4, '4 - Хорошо'), (3, '3 - Удовлетворительно'), (2, '2 - Неудовлетворительно')]
    )
    date = models.DateField(verbose_name="Дата оценки")
    comment = models.TextField(verbose_name="Комментарий учителя", blank=True)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Учитель")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"
        ordering = ['-date', 'student']

    def __str__(self):
        return f"{self.student} - {self.subject}: {self.score} ({self.date})"