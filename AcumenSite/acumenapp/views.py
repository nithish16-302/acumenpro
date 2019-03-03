from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.core.mail import EmailMessage
import pyqrcode as pyq

from .models import Profile
# Create your views here.
def home(request,*args,**kwargs):
    if request.user.is_authenticated:
        user = request.user
        return render(request,'acumenapp/home.html',{'user':user})
    else:
        return render(request, 'acumenapp/home.html',{})
def events(request):
    return render(request,'acumenapp/events.html',{})
def sponsers(request):
    return render(request,'acumenapp/sponsers.html',{})
def team(request):
    return render(request,'acumenapp/team.html',{})
def register(request):
    if request.method == 'POST':
        emailid = request.POST.get("email")
        username = request.POST.get('userName')
        password = request.POST.get('password')
        mobile_number = request.POST.get('mobileNo')
        user = User.objects.create_user(username=emailid, email=emailid, password=password, first_name=username)
        profile =  Profile(user=user,phone_number =mobile_number)
        qrcode = 'VCEIT' + get_random_string(5).lower()
        sample = pyq.create(qrcode)
        sample.png(qrcode + '.png', scale=10)
        mail_subject = 'Activate your AcumenIT account.'
        message = 'Your Qr is:'
        email = EmailMessage(
            mail_subject, message, to=[emailid]
        )
        email.attach_file('VCEIT0wvfm.png')
        email.send()
        login(request, user)
        return redirect("/home?redirect=true&registered=true")
        pass

def logout_view(request):
    logout(request)
    return redirect('/')