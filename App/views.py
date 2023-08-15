from django.contrib.auth import login, logout,authenticate
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
                return redirect('/home')
            else:
                messages.error(request,"Invalid username or password")
        else:
                messages.error(request,"Invalid username or password")
    return render(request, 'login.html',
    context={'form':AuthenticationForm()})

def logout_view(request):
    logout(request)
    return redirect('../login/')









































# from django.shortcuts import redirect, render, HttpResponse
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required


# # Create your views here.
# @login_required(login_url='login')
# def homePage(request):
#     return render(request, 'index.html')


# def logInPage(request):
#     if request.method == 'POST':
#         login_username = request.POST.get('username')
#         login_password = request.POST.get('password')

#         user = authenticate(request, username=login_username, password=login_password)
#         if user is not None:
#             login(request, user)
#             return redirect('home')
#         else:
#             return HttpResponse("Username password is incorrect!!!")
#     return render(request, 'login.html')


# def signUpPage(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         usertype = request.POST.get('usertype')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         cnf_password = request.POST.get('cnf-password')

#         if password != cnf_password:
#             return HttpResponse("You Password and confirm was not same")
#         else:
#             my_user = User.objects.create_user(username, email, password)
#             my_user.save()
#             return redirect('login')
#     return render(request, 'sign-up.html')


# def logOutPage(request):
#     logout(request)
#     return redirect('login')
