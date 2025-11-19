from django.db.models.signals import post_save
from django.dispatch import receiver
from profiles.models import Profile
from .models import SavedSearch
from accounts.models import Notification


@receiver(post_save, sender=Profile)
def notify_saved_search_matches(sender, instance, created, **kwargs):
    """When a Profile is saved, check active SavedSearches and create Notifications for recruiters when there's a match.

    Simple matching logic (MVP): if any skill in saved_search.skills exists in profile.skills_list OR any keyword in saved_search.keywords is in profile.headline.
    """
    if not instance.is_public:
        return

    profile_skills = {s.strip().lower() for s in instance.skills_list()}
    headline = (instance.headline or '').lower()

    for ss in SavedSearch.objects.filter(active=True):
        # avoid matching the recruiter's own saved searches if they are the same user
        # build search term sets
        ss_skills = {s.strip().lower() for s in (ss.skills or '').split(',') if s.strip()}
        ss_keywords = [k.strip().lower() for k in (ss.keywords or '').split(',') if k.strip()]
        ss_projects = [p.strip().lower() for p in (ss.projects or '').split(',') if p.strip()]
        ss_location = (ss.location or '').strip().lower()

        matched = False
        if ss_skills and (ss_skills & profile_skills):
            matched = True
        # match keywords in headline
        if not matched and ss_keywords:
            for kw in ss_keywords:
                if kw in headline:
                    matched = True
                    break

        # match project keywords against headline or skills
        if not matched and ss_projects:
            for pk in ss_projects:
                if pk in headline or pk in profile_skills:
                    matched = True
                    break

        # location matching best-effort: check if saved location appears in headline
        if not matched and ss_location:
            if ss_location in headline:
                matched = True

        if matched:
            # avoid duplicate notifications for same saved_search & profile
            exists = Notification.objects.filter(user=ss.recruiter, saved_search=ss, profile=instance).exists()
            if not exists:
                msg = f"New candidate match for '{ss.name}': {instance.user.username}"
                Notification.objects.create(user=ss.recruiter, message=msg, saved_search=ss, profile=instance)
