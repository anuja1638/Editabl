from django.shortcuts import render
from postManagement.models import Post

# Create your views here.
def userProfileView(request):
    userPosts = Post.objects.filter(user=request.user)
    return render(request, template_name='userProfile/userProfilePage.html', context={'posts': userPosts})
