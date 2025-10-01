from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe
from .models import CustomUser
from django import forms
from django.contrib.auth.forms import UserCreationForm
class CustomErrorList(ErrorList):
    def __str__(self):
        if not self:
            return ''
        return mark_safe(''.join([
            f'<div class="alert alert-danger" role="alert">{e}</div>' for e in self]))


# class CustomUserCreationForm(UserCreationForm):
#     def __init__(self, *args, **kwargs):
#         super(CustomUserCreationForm, self).__init__(*args, **kwargs)
#         for fieldname in ['username', 'role', 'password1','password2']:
#             self.fields[fieldname].help_text = None
#             self.fields[fieldname].widget.attrs.update(
#                 {'class': 'form-control'}
#             )


class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = (
        (CustomUser.Roles.SEEKER, 'Sign up as a Seeker'),
        (CustomUser.Roles.RECRUITER, 'Sign up as a Recruiter'),
    )

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.RadioSelect,
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        # FIX: This now correctly ADDS the 'role' field to the parent's fields.
        fields = UserCreationForm.Meta.fields + ('role',)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Using your cleaner method to apply the CSS class to all fields.
        # This correctly uses 'password1' and 'password2'.
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].widget.attrs.update({
                'class': 'form-control'
            })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user