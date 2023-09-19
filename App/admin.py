from django.contrib import admin
from .models import User, JobSeeker, JobSeekerAddress, JobSeekerEducation, JobSeekerWorkExperience, Hirer, HirerPost

class UserAdmin(admin.ModelAdmin):
    list_display=('username', 'is_superuser', 'is_jobseeker', 'is_hirer', 'name', 'email', 'phone_number')
admin.site.register(User, UserAdmin)


class JobSeekerAdmin(admin.ModelAdmin):
    list_display=('user', 'profile_image', 'skills', 'about', 'file')
admin.site.register(JobSeeker, JobSeekerAdmin)


admin.site.register(JobSeekerAddress)

admin.site.register(JobSeekerEducation)
admin.site.register(JobSeekerWorkExperience)
# admin.site.register(Resume)

class HirerAdmin(admin.ModelAdmin):
    list_display=('user', 'company_name')
admin.site.register(Hirer, HirerAdmin)


admin.site.register(HirerPost)




