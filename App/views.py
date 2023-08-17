from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.generic import CreateView
from .form import JobSeekerSignUpForm, HirerSignUpForm
from django.contrib.auth.forms import AuthenticationForm
from .models import User
from App.models import Hirer, Job_Seeker
from django.contrib.auth.decorators import login_required

def register(request):
    return render(request, 'register.html')

class job_seeker_register(CreateView):
    model = User
    form_class = JobSeekerSignUpForm
    template_name = 'job_seeker_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('../login/')

class hirer_register(CreateView):
    model = User
    form_class = HirerSignUpForm
    template_name = 'hirer_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('../login')


def login_request(request):
    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None :
                login(request,user)
                return redirect('/')
            else:
                messages.error(request,"Invalid username or password")
        else:
                messages.error(request,"Invalid username or password")
    return render(request, 'login.html', context={'form':AuthenticationForm()})

def logout_view(request):
    logout(request)
    return redirect('../login/')


@login_required(login_url='../login')
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