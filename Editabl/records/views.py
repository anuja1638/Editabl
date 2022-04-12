import imp
from re import sub
from django.shortcuts import render
from .models import abousUsModal
from django.http import HttpResponseRedirect
from utils.mailingUtils import Mailer

# Create your views here.
MAILING_LIST = ['editablServer@gmail.com']
CC_LIST = ['anuja7385@gmail.com',
           'kaustubhchaudhari121@gmail.com',
           'vtohal@gmail.com',
           'jangdekaustubh@gmail.com',
           ]
MAIL_MESSAGE = "Hi Developers,\n\n"\
        "[{}] wants to contact regarding Editabl app.\n"\
        "Details are -\n"\
        "Email - [{}]\n"\
        "Phone - [{}]\n"\
        "Message - [{}]\n\n"\
        "Regards,\n"\
        "Editabl Bot.\n"

def aboutUsView(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        contactData = abousUsModal(name = name,
                                   email = email,
                                   phone = phone,
                                   message = message)
        contactData.save()
        with Mailer() as mailer:
            mailer.sendMail(toAddr = MAILING_LIST,
                            ccAddr = CC_LIST,
                            subject = f"{name} wants to contact for Editabl!", 
                            message=MAIL_MESSAGE.format(name, email, phone, message))
            print(MAIL_MESSAGE)
        return HttpResponseRedirect('/')
    return render(request, template_name='records/aboutUsPage.html', context={})
