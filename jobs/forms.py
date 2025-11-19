from django import forms
from .models import Job

from .locationService import LocationService


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            "title",
            "skills",
            "location",
            "salary",
            "is_remote",
            "visa_sponsorship",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g., Senior Software Engineer, Marketing Manager",
                    "maxlength": "200",
                }
            ),
            "skills": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g., Python, Django, React, JavaScript, Project Management",
                    "rows": 4,
                    "help_text": "List the key skills required for this position, separated by commas.",
                }
            ),
            "location": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g., San Francisco, CA or New York, NY",
                    "maxlength": "300",
                }
            ),
            "salary": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g., 75000",
                    "min": "0",
                    "step": "1000",
                }
            ),
            "is_remote": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "visa_sponsorship": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
        }

        labels = {
            "title": "Job Title",
            "skills": "Required Skills",
            "location": "Location",
            "salary": "Annual Salary (USD)",
            "is_remote": "Remote Work Available",
            "visa_sponsorship": "Visa Sponsorship Available",
        }

        help_texts = {
            "title": "Enter a clear, descriptive job title that candidates will easily understand.",
            "skills": "List the essential skills, technologies, and qualifications needed for this role.",
            "location": "Specify the city and state where this position is based.",
            "salary": "Enter the annual salary amount in USD. This helps attract qualified candidates.",
            "is_remote": "Check this box if the position allows remote work or is fully remote.",
            "visa_sponsorship": "Check this box if your company can sponsor work visas for international candidates.",
        }

    def clean_location(self):
        location = self.cleaned_data.get("location")

        print("new job location is ...", location)
        validated_data = LocationService().get_location(location)
        if not validated_data:
            raise forms.ValidationError(
                "Invalid Location! Please enter a valid address."
            )

        # Return the formatted (validated) display name
        return validated_data[0]["display_name"]
