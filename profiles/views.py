from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Profile
from .forms import ProfileForm, EducationFormSet, ExperienceFormSet, LinkFormSet

User = get_user_model()


def profile_detail(request, username):
    user = get_object_or_404(User, username=username)
    profile = getattr(user, 'profile', None)
    if not profile or (not profile.is_public and request.user != user):
        return render(request, 'profiles/profile_private.html', {'user': user})
    return render(request, 'profiles/profile_detail.html', {'profile': profile})


@login_required
def profile_edit(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        edu_fs = EducationFormSet(request.POST, instance=profile)
        exp_fs = ExperienceFormSet(request.POST, instance=profile)
        link_fs = LinkFormSet(request.POST, instance=profile)
        if form.is_valid() and edu_fs.is_valid() and exp_fs.is_valid() and link_fs.is_valid():
            form.save()
            edu_fs.save()
            exp_fs.save()
            link_fs.save()
            return redirect('profiles:detail', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
        edu_fs = EducationFormSet(instance=profile)
        exp_fs = ExperienceFormSet(instance=profile)
        link_fs = LinkFormSet(instance=profile)
    return render(request, 'profiles/profile_form.html', {'form': form, 'edu_fs': edu_fs, 'exp_fs': exp_fs, 'link_fs': link_fs})
