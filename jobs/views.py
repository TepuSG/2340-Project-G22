from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy
from .forms import JobForm
from .models import Job
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from application.models import Application
from django.contrib.auth import get_user_model


def available_jobs(request):
    # Reuse the home.index template rendering pattern

    if request.user.is_authenticated and request.user.is_recruiter:
        print("recruiter here ")
        return recruiter_jobs(request)

    template_data = {}
    template_data["jobs"] = Job.objects.all()

    template_data["title"] = "Available Jobs"

    return render(request, "jobs/index.html", {"template_data": template_data})


def filters(request):
    from home.filters import FilterOrchestrator

    print(request, request.GET)
    # Get all jobs filtered
    jobs_or_ai = FilterOrchestrator().apply_filters(Job.objects.all(), request.GET)

    template_data = {
        "title": "Filtered Jobs",
        "jobs": [],
        "ai_resp": None,
        "name": None,
        "prompt": None,
    }

    # Determine if this is AI search or regular search
    if request.GET:
        query_key = list(request.GET.keys())[0]  # usually 'ai' or 'search'
        template_data["name"] = query_key
        template_data["prompt"] = request.GET.get(query_key)

    if template_data["name"] == "ai":
        # Store AI response for chat-style display
        template_data["ai_resp"] = jobs_or_ai
    else:
        # Normal job list
        template_data["jobs"] = jobs_or_ai

    print("rednering the jobs", template_data)

    return render(request, "jobs/index.html", {"template_data": template_data})


@login_required
def post_job(request):
    # Only allow recruiters
    if not request.user.is_recruiter:
        return redirect("home.index")  # or return HttpResponseForbidden()

    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)  # don't save yet
            job.recruiter = request.user  # assign logged-in recruiter
            job.save()  # now save
            return redirect("jobs.index")  # redirect after posting
    else:
        form = JobForm()

    return render(request, "jobs/post_job.html", {"form": form})


@method_decorator(login_required, name="dispatch")
class JobUpdateView(UpdateView):
    model = Job
    form_class = JobForm
    template_name = "jobs/edit_job.html"
    success_url = reverse_lazy("recruiter_jobs")

    def get_queryset(self):
        # Only allow the logged-in recruiter to edit their own postings
        return Job.objects.filter(recruiter=self.request.user)


# displays jobs only posted by the current recruiter
@login_required
def recruiter_jobs(request):
    jobs = Job.objects.filter(recruiter=request.user)

    # Calculate statistics
    total_jobs = jobs.count()
    remote_jobs = jobs.filter(is_remote=True).count()
    visa_jobs = jobs.filter(visa_sponsorship=True).count()

    context = {
        "jobs": jobs,
        "total_jobs": total_jobs,
        "remote_jobs": remote_jobs,
        "visa_jobs": visa_jobs,
    }

    return render(request, "jobs/recruiter_jobs.html", context)


@login_required
def job_applicants_pipeline(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # Only allow the recruiter who owns the job to see applicants
    if job.recruiter != request.user:
        return HttpResponseForbidden(
            "You do not have permission to view this job's applicants."
        )

    status_columns = [
        (status_key, label, job.applications.filter(status=status_key))
        for status_key, label in Application.STATUS_CHOICES
    ]

    context = {
        "job": job,
        "status_columns": status_columns,
    }

    return render(request, "jobs/applicant_pipeline.html", context)


@login_required
@require_POST
def update_application_status(request, application_id, new_status):
    app = get_object_or_404(Application, id=application_id)

    # Ensure the user owns this job
    if app.job.recruiter != request.user:
        return HttpResponseForbidden()

    # Validate new status
    valid_statuses = [s[0] for s in Application.STATUS_CHOICES]
    if new_status not in valid_statuses:
        return HttpResponse("Invalid status", status=400)

    app.status = new_status
    app.save()

    # Render a partial card for HTMX update
    return render(request, "jobs/components/application_card.html", {"app": app})


# views.py
from django.http import JsonResponse
from .locationService import LocationService  # your LocationService class


def location_search(request):
    query = request.GET.get("q", "")
    if not query:
        return JsonResponse([], safe=False)

    service = LocationService()
    result = service.get_best_locations(query)

    print("results for the query loc", result)

    # Return the first match or empty
    return JsonResponse(result if result else [], safe=False)


from jobs.models import Job  # replace with your model


def job_search_suggestions(request):
    query = request.GET.get("q", "").strip()
    if not query:
        return JsonResponse([], safe=False)

    # Simple search by title (case-insensitive)
    jobs = Job.objects.filter(title__icontains=query)[:5]

    results = [{"id": job.id, "title": job.title} for job in jobs]

    return JsonResponse(results, safe=False)
