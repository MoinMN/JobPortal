from django.contrib import admin
from .models import User, JobSeeker, JobSeekerAddress, JobSeekerEducation, JobSeekerWorkExperience, Hirer, HirerPost

admin.site.register(User)

admin.site.register(JobSeeker)
admin.site.register(JobSeekerAddress)
admin.site.register(JobSeekerEducation)
admin.site.register(JobSeekerWorkExperience)


admin.site.register(Hirer)


admin.site.register(HirerPost)