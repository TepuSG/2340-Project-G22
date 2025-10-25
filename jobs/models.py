from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.


class Job(models.Model):
    title = models.CharField(max_length=200)
    skills = models.TextField()
    location = models.CharField(max_length=300)
    salary = models.IntegerField()
    is_remote = models.BooleanField(default=False) 
    visa_sponsorship = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)

    
    # links the recruiter to the job
    recruiter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='jobs'
    )

    def __str__(self):
        return f"{self.title} ({self.recruiter.username})"