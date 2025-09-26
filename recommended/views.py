from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from home.models import Job


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

