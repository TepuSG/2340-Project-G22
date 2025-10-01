# users/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    class Roles(models.TextChoices):
        SEEKER = 'SEEKER', 'Seeker'
        RECRUITER = 'RECRUITER', 'Recruiter'

    # This is the crucial field
    role = models.CharField(max_length=10, choices=Roles.choices)

    # You can add helper properties to make your code cleaner
    @property
    def is_seeker(self):
        return self.role == self.Roles.SEEKER

    @property
    def is_recruiter(self):
        return self.role == self.Roles.RECRUITER


class SeekerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='seeker')
    distance = models.IntegerField(default=25)#preferred distance 

    def __str__(self):
        return f"{self.user.username} - Seeker"

    def is_distance_okay(self, distance):
        return self.distance >= distance

class RecruiterProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recruiter')

    def __str__(self):
        return f"{self.user.username} - Recruiter"