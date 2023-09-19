from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404, HttpResponseRedirect
from django.contrib import messages
from django.views.generic import CreateView
from .form import JobSeekerSignUpForm, HirerSignUpForm
from django.contrib.auth.forms import AuthenticationForm
from .models import User
from App.models import Hirer, JobSeeker, JobSeekerAddress, JobSeekerEducation, JobSeekerWorkExperience
from django.contrib.auth.decorators import login_required


from django.contrib.auth.forms import UserCreationForm



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
        user_job_seeker = JobSeeker.objects.get(user=request.user)
        user_job_seeker_address = JobSeekerAddress.objects.filter(jobSeeker=user_job_seeker).first()
        user_job_seeker_education = JobSeekerEducation.objects.filter(jobSeeker=user_job_seeker).all()
        user_job_seeker_experience = JobSeekerWorkExperience.objects.filter(jobSeeker=user_job_seeker).all()
        context = {
            'skills': user_job_seeker.skills.split(','),
            'user_job_seeker': user_job_seeker,
            'user_job_seeker_address': user_job_seeker_address,
            'user_job_seeker_education': user_job_seeker_education,
            'user_job_seeker_experience': user_job_seeker_experience
        }

        if request.method == 'POST':
            if 'form_img' in request.POST:
                profile_img = request.FILES['imageInput']

                user_job_seeker = JobSeeker.objects.get(user=request.user)

                user_job_seeker.profile_image = profile_img

                user_job_seeker.save()
            elif 'form1_submit' in request.POST:
                username = request.POST['username']
                name = request.POST['name']
                email = request.POST['email']
                phone_number = request.POST['phone_number']
                date_of_birth = request.POST['date_of_birth']

                user_job_seeker = JobSeeker.objects.get(user=request.user)

                user_job_seeker.user.name = name
                user_job_seeker.user.email = email
                user_job_seeker.user.phone_number = phone_number
                user_job_seeker.date_of_birth = date_of_birth
                # user_job_seeker.about = about

                user_job_seeker.save()

                if User.objects.filter(username=username).exists() and username!=request.user.username:
                    context = {
                        'user_job_seeker': user_job_seeker,
                        'error': "Username Already Exist"
                    }
                    # return render(request, 'newProfile.html', context)
                else:
                    user_job_seeker.user.username = username

                user_job_seeker.user.save()

            elif 'form2_submit' in request.POST:
                about = request.POST['about']
                skills = request.POST['skills']

                user_job_seeker = JobSeeker.objects.get(user=request.user)

                if request.FILES:
                    resume = request.FILES['file']
                    user_job_seeker.file = resume

                user_job_seeker.about = about
                user_job_seeker.skills = skills

                user_job_seeker.save()

            elif 'form3_submit' in request.POST:
                street_address = request.POST['street_address']
                city = request.POST['city']
                state = request.POST['state']
                postal_code = request.POST['postal_code']
                country = request.POST['country']

                user_job_seeker_address, user_job_seeker_address_create = JobSeekerAddress.objects.get_or_create(jobSeeker_id=request.user.id)

                user_job_seeker_address.street_address = street_address
                user_job_seeker_address.city = city
                user_job_seeker_address.state = state 
                user_job_seeker_address.postal_code = postal_code
                user_job_seeker_address.country = country

                user_job_seeker_address.save()

            elif 'form4_submit' in request.POST:
                school_name = request.POST['school_name']
                field_of_study = request.POST['field_of_study']
                degree = request.POST['degree']
                start_date = request.POST['start_date_edu']
                end_date = request.POST['end_date_edu']


                # user_job_seeker_education, user_job_seeker_education_create = JobSeekerEducation.objects.get_or_create(jobSeeker_id=request.user.id)
                user_job_seeker_education = JobSeekerEducation.objects.create(jobSeeker_id=request.user.id)

                user_job_seeker_education.school_name = school_name
                user_job_seeker_education.field_of_study = field_of_study
                user_job_seeker_education.degree = degree
                user_job_seeker_education.start_date = start_date
                user_job_seeker_education.end_date = end_date

                user_job_seeker_education.save()

            elif 'form5_submit' in request.POST:
                company_name = request.POST['company_name']
                position = request.POST['position']
                start_date = request.POST['start_date_exp']
                end_date = request.POST['end_date_exp']
                description = request.POST['description_exp']

                user_job_seeker_expreience = JobSeekerWorkExperience.objects.create(jobSeeker_id=request.user.id)

                user_job_seeker_expreience.company_name = company_name
                user_job_seeker_expreience.position = position
                user_job_seeker_expreience.start_date = start_date
                user_job_seeker_expreience.end_date = end_date
                user_job_seeker_expreience.description = description

                user_job_seeker_expreience.save()
            else:
                print(request.FILES['imageInput'])
                
            return redirect('../profile')
        
    if request.user.is_hirer:
        user_hirer = Hirer.objects.get(user=request.user)
        # Hirer.objects.update()
        context = {
            'user_hirer': user_hirer
        }

    return render(request, 'newProfile.html', context)

@login_required(login_url='../login')
def update_profile(request):
    if request.user.is_jobseeker:
        user_job_seeker = JobSeeker.objects.get(user=request.user)
        context = {
            'user_job_seeker': user_job_seeker
        }

        if request.method == 'POST':                      
            username = request.POST['username']
            name = request.POST['name']
            # last_name = request.POST['last_name']
            email = request.POST['email']
            phone_number = request.POST['phone_number']
            # location = request.POST['location']

            user_job_seeker = JobSeeker.objects.get(user=request.user)

            user_job_seeker.user.name = name
            # user_job_seeker.user.last_name = last_name
            user_job_seeker.user.email = email
            user_job_seeker.user.phone_number = phone_number
            # user_job_seeker.location = location

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
            name = request.POST['name']
            # last_name = request.POST['last_name']
            email = request.POST['email']
            phone_number = request.POST['phone_number']
            # designation = request.POST['designation']

            user_hirer = Hirer.objects.get(user=request.user)

            user_hirer.user.name = name
            # user_hirer.user.last_name = last_name
            user_hirer.user.email = email
            user_hirer.user.phone_number = phone_number
            # user_hirer.designation = designation

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
    



# @login_required(login_url='../login')
# def upload_resume(request):
#     if request.method == 'POST':
#         form = ResumeForm(request.POST, request.FILES)
#         if form.is_valid():
#             resume = form.save(commit=False)
#             resume.jobSeeker_id = request.user.id
#             resume.save()
#             return HttpResponse('success')
#     else:
#         form = ResumeForm()
#     return render(request, 'upload_resume.html', {'form': form})