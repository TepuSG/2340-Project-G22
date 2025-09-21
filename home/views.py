from django.shortcuts import render
from .models import Job

def index(request, **kwargs):
    template_data = {}
    template_data['title'] = 'Job Board Home'
    load_extra_context(kwargs, template_data)
    print('template data for index is', template_data)
    return render(request, 'home/index.html', {'template_data': template_data})


def load_extra_context(kwargs, template_data):
    for key, value in kwargs.items():
        template_data[key] = value
    return template_data


def filters(request):
    from .filters import FilterOrchestrator

    jobs = FilterOrchestrator().apply_filters(Job.objects.all(), request.GET)

    return index(request, jobs=jobs)


