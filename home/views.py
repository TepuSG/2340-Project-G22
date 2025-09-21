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


def search(request):
    name = request.GET.get('search')
    jobs = Job.objects.all()
    if name:
        jobs = jobs.filter(title__icontains=name)
    print('found jobs:', jobs)
    return index(request, jobs=jobs)

def filters(request):
    jobs = Job.objects.all()
    
    title = request.GET.get('title')
    location = request.GET.get('location')
    min_salary = request.GET.get('min_salary')
    max_salary = request.GET.get('max_salary')
    remote = request.GET.get('remote')
    visa_sponsorship = request.GET.get('visa')

    print('filter params:', 'title', title, 'location', location, 'remote', remote, 'visa_sponsorship', visa_sponsorship)

    if title:
        jobs = jobs.filter(title__icontains=title)
    if location:
        jobs = jobs.filter(location__icontains=location)
    if min_salary and min_salary.isdigit():
        jobs = jobs.filter(salary__gte=int(min_salary))
    if max_salary and max_salary.isdigit():
        jobs = jobs.filter(salary__lte=int(max_salary))
    if remote in ['true', 'false']:
        jobs = jobs.filter(is_remote=(remote == 'true'))
    if visa_sponsorship in ['true', 'false']:
        jobs = jobs.filter(visa_sponsorship=(visa_sponsorship == 'true'))

    print('filtered jobs:', jobs)
    return index(request, jobs=jobs)

