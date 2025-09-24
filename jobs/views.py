from django.shortcuts import render
from home.models import Job


def available_jobs(request):
    # Reuse the home.index template rendering pattern
    template_data = {}
    template_data['title'] = 'Available Jobs'
    template_data['jobs'] = Job.objects.all()
    return render(request, 'jobs/index.html', {'template_data': template_data})


def filters(request):
    from home.filters import FilterOrchestrator

    jobs = FilterOrchestrator().apply_filters(Job.objects.all(), request.GET)

    template_data = {}
    template_data['title'] = 'Filtered Jobs'
    template_data['jobs'] = jobs

    return render(request, 'jobs/index.html', {'template_data': template_data})
