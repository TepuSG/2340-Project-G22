from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponseForbidden
from jobs.models import Job
from django.db import models
from mapbox_location_field.models import LocationField
from accounts.decorators import seeker_required
from accounts.models import SeekerProfile
from .models import CityPreference
from .cities import get_city_coordinates, get_cities_list
import json
import math


class SomeLocationModel(models.Model):
    location = LocationField()


def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points using Haversine formula"""
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.asin(math.sqrt(a))

    # Radius of earth in miles
    r = 3956
    return c * r


def index(request):
    # Get user's city preference if authenticated
    city_preference = None
    selected_city_coords = None

    if request.user.is_authenticated:
        try:
            city_preference = CityPreference.objects.get(user=request.user)
        except CityPreference.DoesNotExist:
            # Create default preference
            city_preference = CityPreference.objects.create(
                user=request.user, selected_city="N/A", radius_miles=25
            )

        # Get coordinates for the selected city
        lat, lng = get_city_coordinates(city_preference.selected_city)
        if lat and lng:
            selected_city_coords = {"lat": lat, "lng": lng}

    # Collect all jobs with basic fields
    jobs_qs = Job.objects.all().values("id", "title", "location", "salary", "is_remote")
    jobs = list(jobs_qs)

    template_data = {
        "title": "Job Map - City-Based Search",
    }

    context = {
        "template_data": template_data,
        "jobs": jobs,
        "jobs_json": json.dumps(jobs),
        "cities_choices": get_cities_list(),
        "city_preference": city_preference,
        "selected_city_coords": selected_city_coords,
        "MAPBOX_KEY": getattr(settings, "MAPBOX_KEY", ""),
    }

    return render(request, "jobmap/index.html", context)


@seeker_required
def update_distance(request):
    print("updatind distance")
    if request.method == "POST":
        if not request.user.is_seeker:
            return HttpResponseForbidden("Only seekers can update preferences.")

        try:
            preferred_distance_str = request.POST.get("preferred_distance", "25")
            print("saving new distance", preferred_distance_str)
            # Handle empty radius - use None for "no radius limit"
            if preferred_distance_str.strip() == "":
                preferred_distance = None
            else:
                preferred_distance = int(preferred_distance_str)
            selected_city = request.POST.get("selected_city", "N/A")

            # Get or create city preference
            city_preference, created = CityPreference.objects.get_or_create(
                user=request.user,
                defaults={
                    "selected_city": selected_city,
                    "radius_miles": preferred_distance,
                },
            )

            # Update the preference
            city_preference.selected_city = selected_city
            city_preference.radius_miles = preferred_distance
            city_preference.save()

        except (TypeError, ValueError):
            return HttpResponseForbidden("Invalid distance value.")

    return redirect("jobmap.index")
