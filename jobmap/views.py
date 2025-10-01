from django.shortcuts import render, redirect
from django.conf import settings
from home.models import Job
from django.db import models
from mapbox_location_field.models import LocationField
from accounts.decorators import seeker_required
from accounts.models import SeekerProfile
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

@seeker_required
def update_distance(request):
    if request.method == "POST":
        print('post')
        if not request.user.is_seeker:
            print('not seeker')
            return HttpResponseForbidden("Only seekers can update distance.")
        try:
            preferred_distance = int(request.POST.get('preferred_distance'))
            print('updating to', preferred_distance, 'from', request.user.seeker)
            
            # request.user.seeker.distance = preferred_distance
            # request.user.seeker.save()
        except (TypeError, ValueError):
            # Bad input (not a number)
            return HttpResponseForbidden("Invalid distance value.")

    return redirect('jobmap.index')
