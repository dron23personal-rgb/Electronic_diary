from django.db import models
from django.contrib.auth.models import User
from core.models import Subject


class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    subjects = models.ManyToManyField(Subject, verbose_name="Преподаваемые предметы", blank=True)
    phone = models.CharField(max_length=20, verbose_name="Телефон", blank=True)
    room_number = models.CharField(max_length=10, verbose_name="Номер кабинета", blank=True)

    class Meta:
        verbose_name = "Профиль учителя"
        verbose_name_plural = "Профили учителей"

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"