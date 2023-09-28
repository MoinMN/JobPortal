from nltk.tokenize import sent_tokenize
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponseForbidden, JsonResponse
from App.models import Hirer, JobSeeker, JobSeekerAddress, JobSeekerEducation, JobSeekerWorkExperience, HirerPost, HirerAddress, User, HirerSocialMedia, JobSeekerSocialMedia, JobApplication
from .models import ContactUs
from App.models import HirerPost
from django.contrib.auth.decorators import login_required
from App.form import PostForm, ResponseChoice

from urllib.parse import urlparse
import nltk

# nltk.download('punkt')
# nltk.download('punkt', download_dir=False)



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
        user = User.objects.get(id=request.user.id)
        user_job_seeker = JobSeeker.objects.get(user=request.user)
        user_job_seeker_address = JobSeekerAddress.objects.filter(jobSeeker=user_job_seeker).first()
        job_application = JobApplication.objects.filter(applicant=user_job_seeker)

        user_job_seeker_first_education = JobSeekerEducation.objects.filter(jobSeeker=user_job_seeker).first()
        user_job_seeker_first_experience = JobSeekerWorkExperience.objects.filter(jobSeeker=user_job_seeker).first()

        user_completeness_percentage = user.calculate_user_completeness()
        completeness_percentage_user_job_seeker = user_job_seeker.calculate_jobseeker_completeness()
        if user_job_seeker_address:
            completeness_percentage_user_job_seeker_address = user_job_seeker_address.calculate_jobseekeraddress_completeness()
        else:
            completeness_percentage_user_job_seeker_address = 0

        if user_job_seeker_first_education:
            completeness_percentage_user_job_seeker_first_education = user_job_seeker_first_education.calculate_jobseekereducation_completeness()
        else:
            completeness_percentage_user_job_seeker_first_education = 0

        percentage_user = (user_completeness_percentage + completeness_percentage_user_job_seeker + completeness_percentage_user_job_seeker_address +
                           completeness_percentage_user_job_seeker_first_education ) / 4

        context = {
            'job_application': job_application,

            'user_job_seeker': user_job_seeker,
            'user_job_seeker_address': user_job_seeker_address,
            'user_job_seeker_first_education': user_job_seeker_first_education,

            'percentage_user': percentage_user,
        }

        return render(request, 'home.html', context)

    else:
        user = User.objects.get(id=request.user.id)
        user_hirer = Hirer.objects.get(user=request.user)
        user_hirer_address = HirerAddress.objects.filter(hirer=user_hirer).first()
        user_hirer_posts = HirerPost.objects.filter(hirer_id=request.user.id).all()

        num_applications = 0
        for item in user_hirer_posts:
            job_application = JobApplication.objects.filter(job_post=item.id)
            num_applications += job_application.count()
        
        user_completeness_percentage = user.calculate_user_completeness()
        completeness_percentage_user_hirer = user_hirer.calculate_hirer_completeness()
        if user_hirer_address:
            completeness_percentage_user_hirer_address = user_hirer_address.calculate_hireraddress_completeness()
        else:
            completeness_percentage_user_hirer_address = 0
        percentage_user = (user_completeness_percentage + completeness_percentage_user_hirer + completeness_percentage_user_hirer_address) / 3

        context = {
            'user_hirer': user_hirer,
            'user_hirer_address': user_hirer_address,

            'user_hirer_posts': user_hirer_posts,
            'num_applications': num_applications,

            'percentage_user': percentage_user,
        }

        return render(request, 'home.html', context)


@login_required(login_url='../account/login')
def create_post(request):
    if request.user.is_jobseeker:
        return redirect('home')
    
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            hirer_post = form.save(commit=False)
            hirer_post.hirer = request.user.hirer
            hirer_post.save()
            return redirect('my-post')
    else:
        form = PostForm()

    return render(request, 'createPost.html', {'form': form})


@login_required(login_url='../account/login')
def update_post(request, post_id):
    if request.user.is_jobseeker:
        return redirect('home')
    
    post = get_object_or_404(HirerPost, id=post_id)

    if request.user != post.hirer.user:
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


@login_required(login_url='../account/login')
def delete_post(request, post_id):
    if request.user.is_jobseeker:
        return redirect('home')

    post = get_object_or_404(HirerPost, id=post_id)

    if request.user == post.hirer.user:
        post.delete()
        return redirect('my-post')
    else:
        return HttpResponseForbidden("You do not have permission to delete this post.")


@login_required(login_url='../account/login')
def post_view(request, post_id):    
    post = get_object_or_404(HirerPost, id=post_id)

    if JobApplication.objects.filter(applicant=request.user.id, job_post=post_id).exists():
        has_applied = True
    else:
        has_applied = False


    job_application = 'None'
    user_job_seeker = 'None'
    user_job_seeker_application = 'None'
    if request.user.is_jobseeker:
        user_job_seeker_application = JobApplication.objects.filter(applicant=request.user.id, job_post=post_id)
        user_job_seeker = JobSeeker.objects.get(user=request.user)
    else:
        job_application = JobApplication.objects.filter(job_post_id=post_id)

        if request.method == 'POST':
            for item in job_application:
                key = 'myResponse-' + str(item.id)
                result = request.POST[key]
                application = JobApplication.objects.get(pk=item.id)
                application.response = result
                application.save()
            
            return redirect('view-post', post_id)


    user_hirer = Hirer.objects.get(user=post.hirer.user)
    companyAddress = HirerAddress.objects.filter(hirer=user_hirer).first()
    socialMedia = HirerSocialMedia.objects.filter(hirer=user_hirer).first()

    aboutData = user_hirer.about_company

    if not aboutData is None:
        if '.' in aboutData:
            aboutData = "<p>" + "<br>".join(aboutData.split("\n")) + "</p>"

    purpose = post.job_purpose
    highlight = post.job_highlights
    skills = post.skills_requirement.split(',')

    purposeDatas = sent_tokenize(purpose)

    highlightDatas = sent_tokenize(highlight)

    context = {
        'post': post,

        'user_job_seeker': user_job_seeker,
        'user_job_seeker_application': user_job_seeker_application,

        'has_applied': has_applied,

        'job_application': job_application,

        'user_hirer': user_hirer,
        'company_address': companyAddress,
        'social_media': socialMedia,
        'aboutData': aboutData,

        'purposeDatas': purposeDatas,
        'highlightDatas': highlightDatas,
        'skills': skills,
    }

    return render(request, 'postView.html', context)


@login_required(login_url='../account/login')
def my_post(request):
    if request.user.is_jobseeker:
        return redirect('home')
    
    posts = HirerPost.objects.filter(hirer_id=request.user.id).all()
    
    if posts.exists() == False:
        posts = False

    context = {
        'posts': posts,
    }

    return render(request, 'myPost.html', context)


@login_required(login_url='../account/login')
def find_job(request):
    if request.user.is_hirer:
        return redirect('home')

    posts = HirerPost.objects.all()
    user_job_seeker = JobSeeker.objects.get(user=request.user)

    context = {
        'posts': posts,
        'user_job_seeker': user_job_seeker,
    }

    return render(request, 'findJob.html', context)



@login_required(login_url='../account/login')
def save_post(request, post_id):
    if request.user.is_hirer:
        return redirect('home')

    user_job_seeker = JobSeeker.objects.get(user=request.user)
    post = HirerPost.objects.get(id=post_id)

    previous_url = request.META.get('HTTP_REFERER', None)

    user_job_seeker.saved_posts.add(post)
    
    return redirect(previous_url)


@login_required(login_url='../account/login')
def unsave_post(request, post_id):
    if request.user.is_hirer:
        return redirect('home')

    user_job_seeker = JobSeeker.objects.get(user=request.user)
    post = HirerPost.objects.get(id=post_id)


    user_job_seeker.saved_posts.remove(post)
    previous_url = request.META.get('HTTP_REFERER', None)
    
    return redirect(previous_url)

# hererererererrre
@login_required(login_url='../account/login')
def save_unsave_post(request, post_id):
    user_job_seeker = JobSeeker.objects.get(user=request.user)
    post = HirerPost.objects.get(pk=post_id)

    if user_job_seeker.saved_posts.filter(id=post_id).exists():
        user_job_seeker.saved_posts.remove(post)
        saved = False
    else:
        # Job seeker has not saved the post, so save it
        user_job_seeker.saved_posts.add(post)
        saved = True

    # Return a JSON response indicating success and the updated save status
    data = {'saved': saved}
    return JsonResponse(data)

# hererererererrre


@login_required(login_url='../account/login')
def view_saved_post(request):
    if request.user.is_hirer:
        return redirect('home')
    
    user_job_seeker = JobSeeker.objects.get(user=request.user)
    posts =  user_job_seeker.saved_posts.all()

    context = {
        'posts': posts,
        'user_job_seeker': user_job_seeker,
    }

    return render(request, 'savedNappliedPosts.html', context)


@login_required(login_url='../account/login')
def apply_job(request, post_id):
    if request.user.is_hirer:
        return redirect('home')
    
    user_job_seeker = JobSeeker.objects.get(user=request.user)
    post = HirerPost.objects.get(id=post_id)
    
    jobApplication = JobApplication(applicant=user_job_seeker, job_post=post, resume=user_job_seeker.resume)
    jobApplication.save()

    previous_url = request.META.get('HTTP_REFERER', None)

    return redirect(previous_url)


@login_required(login_url='../account/login')
def applied_job(request):
    if request.user.is_hirer:
        return redirect('home')
    
    user_job_seeker = JobSeeker.objects.get(user=request.user)
    job_application = JobApplication.objects.filter(applicant=user_job_seeker).all()

    saved_post = user_job_seeker.saved_posts.all()

    context = {
        'job_application': job_application,
        'saved_post': saved_post,
    }

    return render(request, 'savedNappliedPosts.html', context)