from django.contrib import admin
from .models import Profile, ProfileEducation, ProfileExperience, ProfileLink


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'headline', 'is_public')


@admin.register(ProfileEducation)
class ProfileEducationAdmin(admin.ModelAdmin):
    list_display = ('profile', 'school', 'degree')


@admin.register(ProfileExperience)
class ProfileExperienceAdmin(admin.ModelAdmin):
    list_display = ('profile', 'company', 'title')


@admin.register(ProfileLink)
class ProfileLinkAdmin(admin.ModelAdmin):
    list_display = ('profile', 'label', 'url')
