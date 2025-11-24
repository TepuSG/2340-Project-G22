from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Profile
from .forms import ProfileForm, EducationFormSet, ExperienceFormSet, LinkFormSet, UserUpdateForm
from jobmap.models import CityPreference

User = get_user_model()


def profile_detail(request, username):
    user = get_object_or_404(User, username=username)
    profile = getattr(user, "profile", None)
    if not profile or (not profile.is_public and request.user != user):
        return render(request, "profiles/profile_private.html", {"user": user})
    return render(request, "profiles/profile_detail.html", {"profile": profile})


@login_required
def profile_edit(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    # Get city preference for both GET and POST
    try:
        city_preference = CityPreference.objects.get(user=request.user)
    except CityPreference.DoesNotExist:
        # Create default preference
        city_preference = CityPreference.objects.create(
            user=request.user, selected_city="N/A", radius_miles=25
        )

    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        form = ProfileForm(request.POST, instance=profile)
        edu_fs = EducationFormSet(request.POST, instance=profile, prefix='education')
        exp_fs = ExperienceFormSet(request.POST, instance=profile, prefix='experience')
        link_fs = LinkFormSet(request.POST, instance=profile, prefix='links')
        if (
            user_form.is_valid()
            and form.is_valid()
            and edu_fs.is_valid()
            and exp_fs.is_valid()
            and link_fs.is_valid()
        ):
            user_form.save()
            form.save()
            edu_fs.save()
            exp_fs.save()
            link_fs.save()
            return redirect("profiles:detail", username=request.user.username)
    else:
        user_form = UserUpdateForm(instance=request.user)
        form = ProfileForm(instance=profile)
        edu_fs = EducationFormSet(instance=profile, prefix='education')
        exp_fs = ExperienceFormSet(instance=profile, prefix='experience')
        link_fs = LinkFormSet(instance=profile, prefix='links')

    return render(
        request,
        "profiles/profile_form.html",
        {
            "user_form": user_form,
            "form": form,
            "edu_fs": edu_fs,
            "exp_fs": exp_fs,
            "link_fs": link_fs,
            "miles": city_preference.radius_miles,
        },
    )
