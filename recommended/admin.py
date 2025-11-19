from django.contrib import admin
from .models import SavedSearch


@admin.register(SavedSearch)
class SavedSearchAdmin(admin.ModelAdmin):
    list_display = ('name', 'recruiter', 'created_at', 'active')
    search_fields = ('name', 'recruiter__username', 'skills', 'keywords', 'location', 'projects')
    list_filter = ('active',)
from django.contrib import admin

# Register your models here.
