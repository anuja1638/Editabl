from django.shortcuts import render

# Create your views here.
def feedPageView(request):
    return render(request, template_name='feed/feedPage.html', context={})
