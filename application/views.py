from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from home.models import Job  # wherever your Job model lives
from .forms import ApplicationForm
from django.contrib import messages
from .models import Application
from django.db import IntegrityError

@login_required
def apply_to_job(request, id):
    job = get_object_or_404(Job, id=id)

    if Application.objects.filter(job=job, job_seeker=request.user).exists():
        messages.warning(request, f"You have already applied to {job.title}.")
        return redirect('jobs.index')

    if request.method == "POST":
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.job_seeker = request.user
            application.status = "applied"   # ensure it starts here
            application.save()
            messages.success(request, f"You applied to {job.title}.")
            return redirect("jobs.index")
    else:
        form = ApplicationForm()

    return render(request, "application/apply.html", {"form": form, "job": job})



@login_required
def my_applications(request):
    applications = Application.objects.filter(job_seeker=request.user).select_related("job")
    return render(request, "application/my_applications.html", {"applications": applications})

