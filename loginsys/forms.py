from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from validate_email import validate_email

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

    def is_valid(self):
        return validate_email(self.email)
