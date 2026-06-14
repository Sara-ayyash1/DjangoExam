from django.shortcuts import render , redirect
from login_app.models import User
from .models import *
from django.contrib import messages
# Create your views here.

def index(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user' : user , 
        'all_books' : .objects.all() , 

    }
    return render(request , 'dashboard.html' , context)


# def (request):
#     if 'user_id' not in request.session:
#         return redirect('/')
#     return
