from django.shortcuts import render
from App.models import Hirer, Job_Seeker
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'index.html')

