from django.db import models
from django.contrib.auth.models import AbstractUser

from uuid import uuid4

class User(AbstractUser):
    is_jobseeker = models.BooleanField(default=False)
    is_hirer = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    # last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)


class JobSeeker(models.Model):
    id = models.UUIDField(default=uuid4, editable=False)
    
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)

    # About me
    about = models.TextField(blank=True, null=True)
    
    # skills
    skills = models.TextField(blank=True, null=True, default='None, ')

    # resume
    # file = models.FileField(upload_to='resumes/')

    # Address
    # jobSeekerAddress = models.ForeignKey(JobSeekerAddress, on_delete=models.CASCADE, null=True, blank=True)

    # Education
    # jobSeekerEducation = models.ManyToManyField(JobSeekerEducation, null=True, blank=True)

    # work experience
    # jobSeekerWorkExperience = models.ManyToManyField(JobSeekerWorkExperience, null=True, blank=True)
    
    def __str__(self):
        return self.user.username



class JobSeekerAddress(models.Model):
    jobSeeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE)

    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.jobSeeker.user.username

class JobSeekerEducation(models.Model):
    jobSeeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE)

    school_name = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    # field_of_study = models.CharField(max_length=100)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.jobSeeker.user.username

class JobSeekerWorkExperience(models.Model):
    jobSeeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE)

    company_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    description = models.TextField()

    def __str__(self):
        return self.jobSeeker.user.username

class Resume(models.Model):
    jobSeeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE)
    file = models.FileField(upload_to='resumes/')


    # def save(self, *args, **kwargs):
    #     # Modify the filename here (e.g., append a timestamp)
    #     import os
    #     from django.utils import timezone

    #     timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    #     filename, file_extension = os.path.splitext(self.file.name)
    #     new_filename = f'{self.jobSeeker.user.username}_{timestamp}{file_extension}'

    #     # Update the file field with the new filename
    #     self.file.name = new_filename

    #     super(Resume, self).save(*args, **kwargs)
    def __str__(self):
        return self.jobSeeker.user.username





class Hirer(models.Model):
    id = models.UUIDField(default=uuid4, editable=False)

    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)

    company_name = models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return self.user.username


class HirerAddress(models.Model):
    hirer = models.ForeignKey(Hirer, on_delete=models.CASCADE)

    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.hirer.user.username


    

class HirerPost(models.Model):
    hire = models.ForeignKey(Hirer, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    content = models.TextField()
    skills_requirement = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    