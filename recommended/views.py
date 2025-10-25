from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from jobs.models import Job


# Create your views here.

@login_required
def index(request):

	user_profile = request.user.profile
	skills_input = user_profile.skills if user_profile else ""

	jobs = None
	if skills_input:
		terms = [t.strip() for t in skills_input.split(",") if t.strip()]
		q = Q()
		for t in terms:
			q |= Q(skills__icontains=t)
		jobs = Job.objects.filter(q).distinct()
	
	return render(request, "recommended/index.html", {"jobs": jobs, "skills": skills_input})


#check that this works???


@login_required
def recruiter_overview(request):
    from profiles.models import Profile

    # Only recruiters may access this overview
    if not getattr(request.user, 'is_recruiter', False):
        return HttpResponseForbidden()

    # Jobs posted by the recruiter
    jobs = Job.objects.filter(recruiter=request.user)
    if not jobs.exists():
        return render(request, 'recommended/recruiter_overview.html', {'jobs': [], 'candidates': []})

    # Collect all skill terms across the recruiter's jobs
    job_skill_terms = set()
    job_skill_map = []  # list of tuples (job, set(skills)) to speed per-job matching
    for j in jobs:
        terms = {s.strip().lower() for s in (j.skills or '').split(',') if s.strip()}
        if terms:
            job_skill_terms.update(terms)
        job_skill_map.append((j, terms))

    if not job_skill_terms:
        return render(request, 'recommended/recruiter_overview.html', {'jobs': jobs, 'candidates': []})

    # Candidate pool
    candidates_qs = Profile.objects.exclude(skills__isnull=True).exclude(skills__exact='')

    matched = []
    for prof in candidates_qs:
        prof_terms = {s.strip().lower() for s in (prof.skills or '').split(',') if s.strip()}
        intersect = job_skill_terms & prof_terms
        if intersect:
            # list job titles that have at least one matching skill with this profile
            matched_jobs = [j.title for (j, jterms) in job_skill_map if jterms & prof_terms]
            matched.append({'profile': prof, 'matches': sorted(intersect), 'matched_jobs': matched_jobs})

    return render(request, 'recommended/recruiter_overview.html', {'jobs': jobs, 'candidates': matched})

