from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import AppUser


class AppUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = AppUser
        fields = ("username", "password1", "password2", "mobile_number", "birth_date")

    def save(self, commit=True):
        user = super(AppUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
