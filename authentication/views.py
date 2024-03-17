from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.templatetags.static import static
from django.core.files.storage import default_storage
from django.conf import settings
import os
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Request, Notification
from django.utils.translation import gettext_lazy as _
from . import candy

# Create your views here.
def home(request):
    return candy.render(request, 'authentication/CrimsonConnect.html')

def auth_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Bad Credentials")
            return redirect('auth_login')

    return render(request, 'authentication/login.html')

def register(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        profile_photo = request.FILES.get('profile_photo')

        if User.objects.filter(username=username):
            messages.error(request, "Username already exists!")
            return redirect('auth_login')

        if User.objects.filter(email=email):
            messages.error(request, "Email already registered!")
            return redirect('auth_login')

        if not phone or len(phone) < 10:
            messages.error(request, "Phone number must be at least 10 digits")
            return redirect('auth_login')

        if not username or len(username) > 15:
            messages.error(request, "Username must be between 1 to 15 characters")
            return redirect('auth_login')

        if not pass1 or len(pass1) < 8:
            messages.error(request, "Password must be at least 8 characters")
            return redirect('auth_login')

        if pass1 != pass2:
            messages.error(request, "Passwords don't match")
            return redirect('auth_login')

        myuser = User.objects.create_user(username=username, email=email, password=pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = True
        myuser.save()
        login(request, myuser)

        user_profile = UserProfile.objects.create(
            user=myuser,
            profile_pic=profile_photo,
            state=None,
            address=None, 
            postcode=None,
            country=None,
            education=None,
            phone=phone
        )
        user_profile.save()

        messages.success(request, "Your account has been successfully created.")

        return redirect('auth_login')

    return render(request, "authentication/register.html")


def signout(request):
    logout(request)
    return redirect('home')

def location(request):
    requests = Request.objects.all().order_by('-request_id')
    return render(request, "authentication/Location.html", {'requests': requests})

@login_required
def viewProfile(request):
    if request.method == 'POST':
        user = request.user
        user_profile = user.userprofile

        # Retrieve original values
        original_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone': user_profile.phone,
            'address': user_profile.address,
            'postcode': user_profile.postcode,
            'state': user_profile.state,
            'country': user_profile.country,
            'education': user_profile.education,
        }

        # Update fields if changed
        # Update fields if changed
        user.first_name = request.POST.get('fname') if request.POST.get('fname') else original_data['first_name']
        user.last_name = request.POST.get('lname') if request.POST.get('lname') else original_data['last_name']
        #print(user.first_name)

        # Update user_profile fields if changed
        user_profile.phone = request.POST.get('phone') if request.POST.get('phone') else original_data['phone']
        user_profile.address = request.POST.get('address') if request.POST.get('address') else original_data['address']
        user_profile.postcode = request.POST.get('postcode') if request.POST.get('postcode') else original_data['postcode']
        user_profile.state = request.POST.get('state') if request.POST.get('state') else original_data['state']
        user_profile.country = request.POST.get('country') if request.POST.get('country') else original_data['country']
        user_profile.education = request.POST.get('education') if request.POST.get('education') else original_data['education']

        user.save()
        user_profile.save()
        return redirect('viewProfile')

    return render(request, "authentication/viewProfile.html")

@login_required()
def requestForm(request):
    if request.method == 'POST':
        requested_blood = request.POST.get('requested_blood')
        recipient_fname = request.POST.get('recipient_fname')
        recipient_pincode = request.POST.get('recipient_pincode')
        recipient_age = request.POST.get('recipient_age')
        relation_with = request.POST.get('relation_with')
        recipient_address = request.POST.get('recipient_address')
        recipient_state = request.POST.get('recipient_state')
        
        # # Debug print statements
        # print("recipient_fname:", recipient_fname)
        # print("recipient_pincode:", recipient_pincode)
        # print("recipient_age:", recipient_age)
        # print("relation_with:", relation_with)
        # print("recipient_address:", recipient_address)
        # print("requested_blood:", requested_blood)
        # print("requested_state:", recipient_state)

        request_instance = Request.objects.create(
            user=request.user,
            requested_blood=requested_blood,
            recipient_fname=recipient_fname,
            recipient_pincode=recipient_pincode,
            recipient_age=recipient_age,
            relation_with=relation_with,
            recipient_address=recipient_address,
            recipient_state=recipient_state
        )
        request_instance.save()

        return redirect('location')
    
    return render(request, "authentication/requestForm.html")

def send_notification(request):
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        donor_user = request.user

        # print(request_id)
        # print(donor_user)

        request_obj = get_object_or_404(Request, request_id=request_id)
        
        notification_instance = Notification.objects.create(
            donor_user=donor_user,
            request_id=request_obj
        )
        notification_instance.save()        
        
    return redirect('location')

def xxnetwork(request):
    return render(request, "authentication/xxnetwork.html")