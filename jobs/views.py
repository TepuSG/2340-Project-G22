from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
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



@method_decorator(login_required, name='dispatch')
class JobUpdateView(UpdateView):
    model = Job
    template_name = 'jobs/edit_job.html'
    fields = ['title', 'skills', 'location', 'salary', 'is_remote', 'visa_sponsorship']
    success_url = reverse_lazy('recruiter_jobs')

    def get_queryset(self):
        # Only allow the logged-in recruiter to edit their own postings
        return Job.objects.filter(recruiter=self.request.user)
    
    
# displays jobs only posted by the current recruiter
@login_required
def recruiter_jobs(request):
    jobs = Job.objects.filter(recruiter=request.user)
    return render(request, 'jobs/recruiter_jobs.html', {'jobs': jobs})