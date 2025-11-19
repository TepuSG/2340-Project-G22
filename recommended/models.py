from django.db import models
from django.conf import settings


class SavedSearch(models.Model):
	"""A saved recruiter candidate search (basic criteria for MVP)."""
	recruiter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_searches')
	name = models.CharField(max_length=200, help_text='Human friendly name for this saved search')
	skills = models.TextField(blank=True, help_text='Comma-separated skills to match')
	keywords = models.TextField(blank=True, help_text='Headline keywords or free text')
	location = models.CharField(max_length=200, blank=True, help_text='Location text (city)')
	projects = models.TextField(blank=True, help_text='Project keyword(s), comma-separated')
	created_at = models.DateTimeField(auto_now_add=True)
	active = models.BooleanField(default=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return f"{self.name} ({self.recruiter.username})"
