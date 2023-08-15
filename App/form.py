from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from .models import User, Job_Seeker, Hirer

class JobSeekerSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    location = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_jobseeker = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        jobseeker = Job_Seeker.objects.create(user=user)
        jobseeker.phone_number=self.cleaned_data.get('phone_number')
        jobseeker.location=self.cleaned_data.get('location')
        jobseeker.save()
        return user

class HirerSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    designation = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_hirer = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        hirer = Hirer.objects.create(user=user)
        hirer.phone_number=self.cleaned_data.get('phone_number')
        hirer.designation=self.cleaned_data.get('designation')
        hirer.save()
        return user
