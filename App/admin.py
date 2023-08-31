from django.contrib import admin
from .models import User, Job_Seeker, Hirer, HirerPost

admin.site.register(User)
admin.site.register(Job_Seeker)
admin.site.register(Hirer)
admin.site.register(HirerPost)