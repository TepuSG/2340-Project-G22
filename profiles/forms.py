from django import forms
from django.forms import inlineformset_factory
from .models import Profile, ProfileEducation, ProfileExperience, ProfileLink


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['headline', 'skills', 'is_public', 'show_skills', 'show_education', 'show_experience', 'show_links']


EducationFormSet = inlineformset_factory(Profile, ProfileEducation, fields=('school','degree','start_year','end_year'), extra=1, can_delete=True)
ExperienceFormSet = inlineformset_factory(Profile, ProfileExperience, fields=('company','title','start_year','end_year','description'), extra=1, can_delete=True)
LinkFormSet = inlineformset_factory(Profile, ProfileLink, fields=('label','url'), extra=1, can_delete=True)
