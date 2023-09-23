from nltk.tokenize import sent_tokenize
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponseForbidden
from App.models import Hirer, JobSeeker, JobSeekerAddress, JobSeekerEducation, JobSeekerWorkExperience, HirerPost, HirerAddress, User
from .models import ContactUs
from App.models import HirerPost
from django.contrib.auth.decorators import login_required
from App.form import PostForm


import nltk

nltk.download('punkt')



def landingPage(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        contact = ContactUs.objects.create()

        contact.name = name
        contact.email = email
        contact.subject = subject
        contact.message = message

        contact.save()

        context = {
            'success': "Thanks for contacting us! We will contact you shortly.",
        }
        return render(request, 'landingPage.html', context)

    return render(request, 'landingPage.html')


@login_required
def view_profile(request, username):

    user_profile = User.objects.get(username=username)

    if user_profile.is_jobseeker:
        user_job_seeker = JobSeeker.objects.get(user=user_profile)
        user_job_seeker_address = JobSeekerAddress.objects.filter(
            jobSeeker=user_job_seeker).first()
        user_job_seeker_education = JobSeekerEducation.objects.filter(
            jobSeeker=user_job_seeker).all()
        user_job_seeker_experience = JobSeekerWorkExperience.objects.filter(
            jobSeeker=user_job_seeker).all()

        context = {
            'user_job_seeker': user_job_seeker,
            'user_job_seeker_address': user_job_seeker_address,
            'user_job_seeker_education': user_job_seeker_education,
            'user_job_seeker_experience': user_job_seeker_experience,
        }

        return render(request, 'viewJobSeekerProfile.html', context)

    if user_profile.is_hirer:
        user_hirer = Hirer.objects.get(user=user_profile)
        user_hirer_address = HirerAddress.objects.filter(
            hirer=user_hirer).first()

        context = {
            'user_hirer': user_hirer,
            'user_hirer_address': user_hirer_address,
        }

        return render(request, 'viewHirerProfile.html', context)


@login_required(login_url='../account/login')
def home(request):
    if request.user.is_jobseeker:
        user_job_seeker = JobSeeker.objects.get(user=request.user)
        user_job_seeker_address = JobSeekerAddress.objects.filter(
            jobSeeker=user_job_seeker).first()

        user_job_seeker_first_education = JobSeekerEducation.objects.filter(
            jobSeeker=user_job_seeker).first()
        user_job_seeker_first_experience = JobSeekerWorkExperience.objects.filter(
            jobSeeker=user_job_seeker).first()

        completeness_percentage_user_job_seeker = user_job_seeker.calculate_jobseeker_completeness()
        if user_job_seeker_address:
            completeness_percentage_user_job_seeker_address = user_job_seeker_address.calculate_jobseekeraddress_completeness()
        else:
            completeness_percentage_user_job_seeker_address = 0

        if user_job_seeker_first_education:
            completeness_percentage_user_job_seeker_first_education = user_job_seeker_first_education.calculate_jobseekereducation_completeness()
        else:
            completeness_percentage_user_job_seeker_first_education = 0

        if user_job_seeker_first_experience:
            completeness_percentage_user_job_seeker_first_experience = user_job_seeker_first_experience.calculate_jobseekerworkexperience_completeness()
        else:
            completeness_percentage_user_job_seeker_first_experience = 0

        percentage_user = (completeness_percentage_user_job_seeker + completeness_percentage_user_job_seeker_address +
                           completeness_percentage_user_job_seeker_first_education + completeness_percentage_user_job_seeker_first_experience) / 4

        context = {
            'user_job_seeker': user_job_seeker,
            'percentage_user': percentage_user,
        }

        return render(request, 'home.html', context)

    else:
        user_hirer = Hirer.objects.get(user=request.user)
        user_hirer_address = HirerAddress.objects.filter(
            hirer=user_hirer).first()

        completeness_percentage_user_hirer = user_hirer.calculate_hirer_completeness()
        if user_hirer_address:
            completeness_percentage_user_hirer_address = user_hirer_address.calculate_hireraddress_completeness()
        else:
            completeness_percentage_user_hirer_address = 0
        percentage_user = (completeness_percentage_user_hirer +
                           completeness_percentage_user_hirer_address) / 2

        context = {
            'user_hirer': user_hirer,
            'percentage_user': percentage_user,
        }

        return render(request, 'home.html', context)


@login_required(login_url='../account/login')
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            hirer_post = form.save(commit=False)
            hirer_post.hire = request.user.hirer
            hirer_post.save()
            return redirect('my-post')
    else:
        form = PostForm()

    return render(request, 'createPost.html', {'form': form})


@login_required(login_url='../account/login')
def update_post(request, post_id):
    post = get_object_or_404(HirerPost, id=post_id)

    if request.user != post.hire.user:
        return HttpResponseForbidden("You do not have permission to edit this post.")

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('my-post')
    else:
        form = PostForm(instance=post)

    # print(form)

    return render(request, 'createPost.html', {'form': form})


def delete_post(request, post_id):
    post = get_object_or_404(HirerPost, id=post_id)

    if request.user == post.hire.user:
        post.delete()
        return redirect('my-post')
    else:
        return HttpResponseForbidden("You do not have permission to delete this post.")


@login_required(login_url='../account/login')
def post_view(request, post_id):
    post = get_object_or_404(HirerPost, id=post_id)
    user_hirer = Hirer.objects.get(user=request.user)
    companyAddress = HirerAddress.objects.filter(hirer=user_hirer).first()

    if request.user != post.hire.user:
        return HttpResponseForbidden("You do not have permission to view this post.")

    aboutData = user_hirer.about_company
    purpose = post.job_purpose
    highlight = post.job_highlights
    skills = post.skills_requirement.split(',')

    if '.' in aboutData:
        aboutData = "<p>" + "<br>".join(aboutData.split("\n")) + "</p>"

    purposeDatas = sent_tokenize(purpose)

    highlightDatas = sent_tokenize(highlight)

    context = {
        'post': post,
        'user_hirer': user_hirer,
        'company_address': companyAddress,

        'aboutData': aboutData,
        'purposeDatas': purposeDatas,
        'highlightDatas': highlightDatas,
        'skills': skills,
    }

    return render(request, 'postView.html', context)


@login_required(login_url='../account/login')
def my_post(request):
    posts = HirerPost.objects.filter(hire_id=request.user.id).all()
    if posts.exists() == False:
        posts = False
    context = {
        'posts': posts,
    }

    return render(request, 'myPost.html', context)


@login_required(login_url='../account/login')
def find_job(request):

    return render(request, 'findJob.html')