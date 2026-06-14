from django.shortcuts import render , redirect
from .models import *
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    return render(request , 'index.html' )

def register(request):
    if request.method == 'POST':
       errors = User.objects.basic_validator(request.POST)

       if len(errors) > 0:
           for msg in errors.values():
               messages.error(request , msg)
           return  redirect('/')
       
       else:
            user = User.objects.create_user(request.POST)
            request.session['user_id']=user.id

            return redirect('/game/dashboard')
    
    return  redirect('/')


def login(request):
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        if errors:
            for msg in errors.values():
                messages.error(request, msg)
            return redirect('/')
        user = User.objects.filter(email=request.POST.get('email', ''))[0]
        request.session['user_id'] = user.id
        return redirect('/game/dashboard')
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def view_profile(request , user_id):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=user_id)
    loginuser = User.objects.get(id=request.session['user_id'])
    return render (request , 'profile.html' , context={'user' :user , 'loginuser' :loginuser})