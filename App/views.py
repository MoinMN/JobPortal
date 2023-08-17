from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.generic import CreateView
from .form import JobSeekerSignUpForm, HirerSignUpForm
from django.contrib.auth.forms import AuthenticationForm
from .models import User

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
