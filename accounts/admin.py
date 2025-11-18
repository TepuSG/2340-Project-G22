from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import CustomUser, SeekerProfile, RecruiterProfile
from .models import Notification

User = get_user_model()

# Custom User Admin for User Story 19: User and Role Management
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    # Add role to the fieldsets
    fieldsets = UserAdmin.fieldsets + (
        ('Role Management', {'fields': ('role',)}),
    )
    
    # Add role to the add form
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role Assignment', {'fields': ('role',)}),
    )
    
    # Actions for managing users
    actions = ['activate_users', 'deactivate_users', 'make_seeker', 'make_recruiter']
    
    def activate_users(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f'{count} users have been activated.')
    activate_users.short_description = "Activate selected users"
    
    def deactivate_users(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f'{count} users have been deactivated.')
    deactivate_users.short_description = "Deactivate selected users"
    
    def make_seeker(self, request, queryset):
        count = queryset.update(role=CustomUser.Roles.SEEKER)
        self.message_user(request, f'{count} users have been changed to Seeker role.')
    make_seeker.short_description = "Change role to Seeker"
    
    def make_recruiter(self, request, queryset):
        count = queryset.update(role=CustomUser.Roles.RECRUITER)
        self.message_user(request, f'{count} users have been changed to Recruiter role.')
    make_recruiter.short_description = "Change role to Recruiter"

# Profile admins
class SeekerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'distance')
    search_fields = ('user__username', 'user__email')
    list_filter = ('distance',)

class RecruiterProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username', 'user__email')

# Register models
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(SeekerProfile, SeekerProfileAdmin)
admin.site.register(RecruiterProfile, RecruiterProfileAdmin)
admin.site.register(Notification)
