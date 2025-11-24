from django.contrib import admin
from django.http import HttpResponse
import csv
from .models import Application


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job_seeker', 'job', 'status', 'applied_at')
    list_filter = ('status', 'applied_at')
    search_fields = ('job_seeker__username', 'job__title')
    actions = ['export_as_csv']
    
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={meta}.csv'
        writer = csv.writer(response)
        
        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])
        
        return response
    export_as_csv.short_description = "Download selected as CSV"


admin.site.register(Application, ApplicationAdmin)
