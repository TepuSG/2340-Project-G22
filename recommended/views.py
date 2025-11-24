from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from jobs.models import Job
from .filters import FilterOrchestrator
from django.shortcuts import redirect
from django.contrib import messages
from .models import SavedSearch


@login_required
def save_search(request):
    # Only recruiters can save searches
    if not getattr(request.user, "is_recruiter", False):
        return HttpResponseForbidden()

    if request.method != "POST":
        return redirect("recommended.candidate_search")

    name = request.POST.get("name", "").strip() or "Saved Search"
    skills = request.POST.get("skills", "").strip()
    keywords = request.POST.get("keywords", "").strip()
    location = request.POST.get("location", "").strip()
    projects = request.POST.get("projects", "").strip()

    SavedSearch.objects.create(
        recruiter=request.user,
        name=name,
        skills=skills,
        keywords=keywords,
        location=location,
        projects=projects,
    )
    messages.success(request, "Search saved successfully.")
    # Redirect back to search with previous filters preserved (if supplied)
    return redirect(request.META.get("HTTP_REFERER", "recommended.candidate_search"))


@login_required
def saved_searches_list(request):
    if not getattr(request.user, "is_recruiter", False):
        return HttpResponseForbidden()

    searches = SavedSearch.objects.filter(recruiter=request.user)
    return render(
        request, "recommended/saved_searches_list.html", {"searches": searches}
    )


@login_required
def delete_saved_search(request, pk):
    if not getattr(request.user, "is_recruiter", False):
        return HttpResponseForbidden()
    ss = get_object_or_404(SavedSearch, pk=pk, recruiter=request.user)
    if request.method == "POST":
        ss.delete()
        messages.success(request, "Saved search deleted")
        return redirect("recommended.saved_searches")
    return render(request, "recommended/confirm_delete.html", {"object": ss})


# Create your views here.


@login_required
def index(request):
    print("laoding recomnded jobss")
    user_profile = request.user.profile
    skills_input = user_profile.skills if user_profile else ""

    jobs = None
    if skills_input:
        terms = [t.strip() for t in skills_input.split(",") if t.strip()]
        q = Q()
        for t in terms:
            q |= Q(skills__icontains=t)
        jobs = Job.objects.filter(q).distinct()
    print(jobs)
    return render(
        request, "recommended/index.html", {"jobs": jobs, "skills": skills_input}
    )


# check that this works???


@login_required
def recruiter_overview(request):
    from profiles.models import Profile
    from django.contrib.auth import get_user_model

    # Only recruiters may access this overview
    if not getattr(request.user, "is_recruiter", False):
        return HttpResponseForbidden()

    User = get_user_model()

    # Jobs posted by the recruiter
    jobs = Job.objects.filter(recruiter=request.user)
    # prepare filter params early so template always has them
    filter_params = {
        "skills": request.GET.get("skills", "").strip(),
        "location": request.GET.get("location", "").strip(),
        "projects": request.GET.get("projects", "").strip(),
    }
    if not jobs.exists():
        return render(
            request,
            "recommended/recruiter_overview.html",
            {"jobs": [], "candidates": [], "filters": filter_params},
        )

    # Collect all skill terms across the recruiter's jobs
    job_skill_terms = set()
    job_skill_map = []  # list of tuples (job, set(skills)) to speed per-job matching
    for j in jobs:
        terms = {s.strip().lower() for s in (j.skills or "").split(",") if s.strip()}
        if terms:
            job_skill_terms.update(terms)
        job_skill_map.append((j, terms))

    if not job_skill_terms:
        return render(
            request,
            "recommended/recruiter_overview.html",
            {"jobs": jobs, "candidates": [], "filters": filter_params},
        )

    # Candidate pool
    candidates_qs = Profile.objects.filter(user__role=User.Roles.SEEKER).exclude(skills__isnull=True).exclude(
        skills__exact=""
    )

    # Apply optional recruiter filters (skills, location, projects) from GET params
    orchestrator = FilterOrchestrator()
    candidates_qs = orchestrator.apply_filters(candidates_qs, filter_params)

    matched = []
    for prof in candidates_qs:
        prof_terms = {
            s.strip().lower() for s in (prof.skills or "").split(",") if s.strip()
        }
        intersect = job_skill_terms & prof_terms
        if intersect:
            # list job titles that have at least one matching skill with this profile
            matched_jobs = [
                j.title for (j, jterms) in job_skill_map if jterms & prof_terms
            ]
            matched.append(
                {
                    "profile": prof,
                    "matches": sorted(intersect),
                    "matched_jobs": matched_jobs,
                }
            )

    # Preserve filter values for the template so the form can show current values
    return render(
        request,
        "recommended/recruiter_overview.html",
        {"jobs": jobs, "candidates": matched, "filters": filter_params},
    )


@login_required
def candidate_search(request):
    """Separate candidate search page for recruiters. Uses the same filters as the overview but is accessible via home button.

    Returns a page with a filter form and results. Only recruiters allowed.
    """
    from profiles.models import Profile
    from django.contrib.auth import get_user_model

    if not getattr(request.user, "is_recruiter", False):
        return HttpResponseForbidden()

    User = get_user_model()

    # Base queryset: show all public seekers by default
    # (Assumption: only public profiles should be visible in search — change to `Profile.objects.all()` if you want truly all)
    candidates_qs = Profile.objects.filter(is_public=True, user__role=User.Roles.SEEKER)

    # Gather filters from GET
    filter_params = {
        "skills": request.GET.get("skills", "").strip(),
        "location": request.GET.get("location", "").strip(),
        "projects": request.GET.get("projects", "").strip(),
    }

    # Apply orchestrator filters
    orchestrator = FilterOrchestrator()
    candidates_qs = orchestrator.apply_filters(candidates_qs, filter_params)

    # For the general search we don't restrict by the recruiter's job skills; instead return any matching candidates
    # Build result list similarly to overview but without matched_jobs context
    results = []
    for prof in candidates_qs:
        prof_terms = {
            s.strip().lower() for s in (prof.skills or "").split(",") if s.strip()
        }
        results.append({"profile": prof, "matches": sorted(prof_terms)})

    return render(
        request,
        "recommended/candidate_search.html",
        {"candidates": results, "filters": filter_params},
    )
