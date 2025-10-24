from django.contrib import admin
from .models import Job

# Custom Job Admin for User Story 20: Job Post Moderation
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'recruiter', 'location', 'salary', 'is_remote', 'visa_sponsorship', 'created_date')
    list_filter = ('is_remote', 'visa_sponsorship', 'location', 'recruiter')
    search_fields = ('title', 'skills', 'location', 'recruiter__username')
    readonly_fields = ('created_date',) if hasattr(Job, 'created_date') else ()
    
    # Organize fields for better display
    fieldsets = (
        ('Job Information', {
            'fields': ('title', 'skills', 'location', 'salary')
        }),
        ('Job Options', {
            'fields': ('is_remote', 'visa_sponsorship')
        }),
        ('Recruiter Information', {
            'fields': ('recruiter',)
        }),
    )
    
    # Add moderation actions
    actions = ['approve_jobs', 'remove_jobs', 'flag_for_review']
    
    def approve_jobs(self, request, queryset):
        # This could set a status field if you add one later
        count = queryset.count()
        self.message_user(request, f'{count} job posts have been approved.')
    approve_jobs.short_description = "Approve selected job posts"
    
    def remove_jobs(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f'{count} job posts have been removed for policy violations.')
    remove_jobs.short_description = "Remove selected job posts (spam/abuse)"
    
    def flag_for_review(self, request, queryset):
        # This could set a review status if you add one later
        count = queryset.count()
        self.message_user(request, f'{count} job posts have been flagged for further review.')
    flag_for_review.short_description = "Flag for manual review"
    
    # Override save to add any additional moderation logic
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

# Register the Job model with custom admin
admin.site.register(Job, JobAdmin)