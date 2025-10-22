from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import JobForm
from .models import Job


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



@login_required
def post_job(request):
    # Only allow recruiters
    if not request.user.is_recruiter:
        return redirect('home.index')  # or return HttpResponseForbidden()

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)   # don't save yet
            job.recruiter = request.user    # assign logged-in recruiter
            job.save()                      # now save
            return redirect('jobs.index')  # redirect after posting
    else:
        form = JobForm()

    return render(request, 'jobs/post_job.html', {'form': form})