from django.db import models
from django.conf import settings
from .cities import get_cities_list

class CityPreference(models.Model):
    """Store user's preferred city and radius for job searching"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='city_preference'
    )
    selected_city = models.CharField(
        max_length=100, 
        choices=get_cities_list(),
        default="N/A",
        help_text="Select a city to center your job search around, or N/A to see all jobs"
    )
    radius_miles = models.PositiveIntegerField(
        default=25,
        null=True,
        blank=True,
        help_text="Search radius in miles from the selected city (leave blank for no limit)"
    )
    
    def __str__(self):
        return f"{self.user.username} - {self.selected_city} ({self.radius_miles} miles)"
    
    class Meta:
        verbose_name = "City Preference"
        verbose_name_plural = "City Preferences"
