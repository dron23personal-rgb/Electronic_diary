from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import TeacherProfile

@receiver(post_save, sender=User)
def create_teacher_profile(sender, instance, created, **kwargs):

    if created:
        TeacherProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_teacher_profile(sender, instance, **kwargs):

    if hasattr(instance, 'teacher_profile'):
        instance.teacher_profile.save()