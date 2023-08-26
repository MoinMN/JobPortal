from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect, render, get_object_or_404, HttpResponseRedirect
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
        # login(self.request, user)
        return redirect('../login/')

class hirer_register(CreateView):
    model = User
    form_class = HirerSignUpForm
    template_name = 'hirer_register.html'

    def form_valid(self, form):
        user = form.save()
        # login(self.request, user)
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
        # Hirer.objects.update()
        context = {
            'user_hirer': user_hirer
        }

    return render(request, 'profile.html', context)

@login_required(login_url='../login')
def update_profile(request):
    if request.user.is_jobseeker:
        user_job_seeker = Job_Seeker.objects.get(user=request.user)
        context = {
            'user_job_seeker': user_job_seeker
        }

        if request.method == 'POST':                      
            username = request.POST['username']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            phone_number = request.POST['phone_number']
            location = request.POST['location']

            user_job_seeker = Job_Seeker.objects.get(user=request.user)


            user_job_seeker.user.first_name = first_name
            user_job_seeker.user.last_name = last_name
            user_job_seeker.email = email
            user_job_seeker.phone_number = phone_number
            user_job_seeker.location = location

            user_job_seeker.save()

            if User.objects.filter(username=username).exists() and username!=request.user.username:
                context = {
                    'user_job_seeker': user_job_seeker,
                    'error': "Username Already Exist"
                }
                return render(request, 'update_profile.html', context)
            

            user_job_seeker.user.username = username
            user_job_seeker.user.save()
            return redirect('../profile') 

    if request.user.is_hirer:
        user_hirer = Hirer.objects.get(user=request.user)
        # Hirer.objects.update()
        context = {
            'user_hirer': user_hirer
        }

        if request.method == 'POST':
            username = request.POST['username']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            phone_number = request.POST['phone_number']
            designation = request.POST['designation']

            user_hirer = Hirer.objects.get(user=request.user)


            user_hirer.user.first_name = first_name
            user_hirer.user.last_name = last_name
            user_hirer.email = email
            user_hirer.phone_number = phone_number
            user_hirer.designation = designation

            user_hirer.save()

            if User.objects.filter(username=username).exists() and username!=request.user.username:
                context = {
                    'user_hirer': user_hirer,
                    'error': "Username Already Exist"
                }
                return render(request, 'update_profile.html', context)
            
            
            user_hirer.user.username = username            
            user_hirer.user.save()

            return redirect('../profile') 

    return render(request, 'update_profile.html', context)
    