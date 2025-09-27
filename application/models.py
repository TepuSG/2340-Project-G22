from django.db import models
from django.conf import settings
from home.models import Job

class Application(models.Model):
    STATUS_CHOICES = [
        ("applied", "Applied"),
        ("review", "Review"),
        ("interview", "Interview"),
        ("offer", "Offer"),
        ("closed", "Closed"),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    job_seeker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="applications"
    )
    note = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="applied")

    class Meta:
        unique_together = ("job", "job_seeker")  # no duplicate apps

    def __str__(self):
        return f"{self.job_seeker} → {self.job.title} ({self.get_status_display()})"
