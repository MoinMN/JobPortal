from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_jobseeker = models.BooleanField(default=False)
    is_hirer = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=60)
    phone_number = models.CharField(max_length=20)


class Job_Seeker(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    location = models.CharField(max_length=20)

    # def __str__(self):
    #     return self.user

class Hirer(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    designation = models.CharField(max_length=20)
    
    # def __str__(self):
    #     return self.user


class HirerPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title