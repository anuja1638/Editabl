from django.shortcuts import render

# Create your views here.
def userProfileView(request):
    return render(request, template_name='userProfile/userProfilePage.html', context={})