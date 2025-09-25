from django.shortcuts import render
from django.conf import settings
from home.models import Job
from django.db import models
from mapbox_location_field.models import LocationField
import json


class SomeLocationModel(models.Model):
    location = LocationField()


def index(request):
    # Collect jobs and pass basic fields to the template. We'll geocode client-side.
    jobs_qs = Job.objects.all().values('id', 'title', 'location')
    jobs = list(jobs_qs)

    template_data = {
        'title': 'Job Map',
    }

    context = {
        'template_data': template_data,
        'jobs': jobs,
        'jobs_json': json.dumps(jobs),
        'MAPBOX_KEY': getattr(settings, 'MAPBOX_KEY', ''),
    }

    return render(request, 'jobmap/index.html', context)
