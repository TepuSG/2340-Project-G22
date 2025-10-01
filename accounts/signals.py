# users/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, SeekerProfile, RecruiterProfile


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == CustomUser.Roles.SEEKER:
            print('seeker created')
            SeekerProfile.objects.create(user=instance)
        elif instance.role == CustomUser.Roles.RECRUITER:
            print('recreuiter created')
            RecruiterProfile.objects.create(user=instance)