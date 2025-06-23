from django import forms
from django.contrib.auth import get_user_model
from .models import Profile

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        # returns the User model that is active in this project
        model = get_user_model()
        fields = ('username', 'first_name', 'email')

    # this method is executed when the form is validated by calling its is_valid() method
    # you can provide a clean_<fieldname> method to any of form fields to clean the value or raise form validation errors for a specific field
    # Forms also include a general clean() method to validate the entire form
    # In this case, we use the field-specific clean method to avoid overriding other field-specific checks set in the model, such as to check username is unique
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Passwords don't match")
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
            model = get_user_model()
            fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
            model = Profile
            fields = ('date_of_birth', 'photo')