from django.shortcuts import render
from App.models import Hirer, Job_Seeker
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'index.html')


@login_required(login_url='../account/login')
def profile(request):
    if request.user.is_jobseeker:
        user_job_seeker = Job_Seeker.objects.get(user=request.user)
        context = {
            'user_job_seeker': user_job_seeker
        }
    if request.user.is_hirer:
        user_hirer = Hirer.objects.get(user=request.user)
        context = {
            'user_hirer': user_hirer
        }    

    return render(request, 'profile.html', context)
