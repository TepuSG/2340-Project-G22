from django.shortcuts import render
from django.db.models import Q

# Create your views here.

def index(request):
	"""Render recommended/index.html and find jobs matching skills input.

	Accepts POST form 'skills' or GET ?skills=...; stores last skills in session.
	"""
	skills_input = request.GET.get("skills") or request.POST.get("skills") or request.session.get("recommended_skills", "")
	jobs = None

	if request.method == "POST" and "skills" in request.POST:
		skills_input = request.POST["skills"]
		request.session["recommended_skills"] = skills_input

	if skills_input:
		# import here to avoid circular imports at module import time
		from home.models import Job
		terms = [t.strip() for t in skills_input.split(",") if t.strip()]
		q = Q()
		for t in terms:
			q |= Q(skills__icontains=t)
		jobs = Job.objects.filter(q).distinct()

	return render(request, "recommended/index.html", {"jobs": jobs, "skills": skills_input})
