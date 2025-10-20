from django import forms
from django.forms import inlineformset_factory
from .models import Profile, ProfileEducation, ProfileExperience, ProfileLink


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['headline', 'skills', 'is_public', 'show_skills', 'show_education', 'show_experience', 'show_links']
        widgets = {
            'headline': forms.TextInput(attrs={'class': 'form-control'}),
            'skills': forms.TextInput(attrs={'class': 'form-control'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'show_skills': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'show_education': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'show_experience': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'show_links': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ProfileEducationForm(forms.ModelForm):
    class Meta:
        model = ProfileEducation
        fields = ['school', 'degree', 'start_year', 'end_year']
        widgets = {
            'school': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'School/University'}),
            'degree': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Degree/Field of Study'}),
            'start_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Start Year'}),
            'end_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'End Year'}),
        }

class ProfileExperienceForm(forms.ModelForm):
    class Meta:
        model = ProfileExperience
        fields = ['company', 'title', 'start_year', 'end_year', 'description']
        widgets = {
            'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job Title'}),
            'start_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Start Year'}),
            'end_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'End Year'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Brief description of your role and accomplishments'}),
        }

class ProfileLinkForm(forms.ModelForm):
    class Meta:
        model = ProfileLink
        fields = ['label', 'url']
        widgets = {
            'label': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., LinkedIn, GitHub, Portfolio'}),
            'url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://example.com'}),
        }


EducationFormSet = inlineformset_factory(Profile, ProfileEducation, form=ProfileEducationForm, extra=1, can_delete=True)
ExperienceFormSet = inlineformset_factory(Profile, ProfileExperience, form=ProfileExperienceForm, extra=1, can_delete=True)
LinkFormSet = inlineformset_factory(Profile, ProfileLink, form=ProfileLinkForm, extra=1, can_delete=True)
