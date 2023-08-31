from django.shortcuts import render
from django.shortcuts import redirect, render, get_object_or_404, HttpResponseRedirect
from App.models import Hirer, Job_Seeker, HirerPost
from django.contrib.auth.decorators import login_required
from App.form import PostForm


# Create your views here.
def index(request):
    return render(request, 'index.html')

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')  # Redirect to a page displaying all posts
    else:
        form = PostForm()
        # print(post.user.username)
    return render(request, 'create_post.html', {'form': form})


@login_required
def post_view(request):
    posts = HirerPost.objects.all()
    return render(request, 'post_view.html', {'posts': posts})



