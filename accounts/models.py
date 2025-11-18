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

    @property
    def unread_notifications_count(self):
        """Return count of unread notifications for this user."""
        try:
            return self.notifications.filter(is_read=False).count()
        except Exception:
            return 0


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


class Notification(models.Model):
    """Simple notification model for users (primarily recruiters)."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:40]}"