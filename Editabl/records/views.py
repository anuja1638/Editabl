from django.shortcuts import render

# Create your views here.

def aboutUsView(request):
    return render(request, template_name='records/aboutUsPage.html', context={})