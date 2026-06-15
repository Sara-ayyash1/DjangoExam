from django.shortcuts import render , redirect
from login_app.models import User
from .models import *
from django.contrib import messages
# Create your views here.

def index(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])

    sort = request.GET.get('sort' , 'name')
    dirc  =  request.GET.get('dir' , 'asc')

    order= f'-{sort}' if dirc == "desc"  else sort

    all_games  = Game.objects.all().order_by(order)

    next_dirc  = 'asc' if dirc == 'desc' else 'asc'
    context = {
        'user' : user , 
        'all_games' : all_games , 
        'sort' :sort,
        'next_dirc' :next_dirc
    }
    return render(request , 'dashboard.html' , context)


def create_game(request):
    if request.method == 'POST':
        if 'user_id' not in request.session:
           return redirect('/')
        
        errors = Game.objects.basic_validator(request.POST)
        
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/game/dashboard')

        Game.objects.create_game(request.POST)
        return redirect('/game/dashboard')
    return redirect('/game/dashboard')


def game_detail(request , game_id):
    if 'user_id' not in request.session:
        return redirect('/')
    
    try:
        game = Game.objects.get(id=game_id)
    except Game.DoesNotExist:
        return redirect('/game/dashboard')
    
    sort = request.GET.get('sort' , 'id')
    dirc  =  request.GET.get('dir' , 'asc')

    order= f'-{sort}' if dirc == "desc"  else sort

    userlikes  = GameLike.objects.filter(game = game ).all().order_by(order)

    next_dirc  = 'asc' if dirc == 'desc' else 'asc'

    context = {
        'game' : game,
        'user':User.objects.get(id=request.session['user_id']),
        'userlikes' : userlikes,
        'sort' :sort,
        'next_dirc' :next_dirc,
    }
    return render(request , 'game_detail.html' , context)

def edit_game(request, game_id):
    if 'user_id' not in request.session:
        return redirect('/')
    
    try:
        game_to_update = Game.objects.get(id=game_id)
    except Game.DoesNotExist:
        return redirect('/game/dashboard')
    
    context = {
        'game' : game_to_update,
        'user':User.objects.get(id=request.session['user_id'])
    }
    return render(request , 'edit_game.html' , context)


def update_game(request, game_id):
    if 'user_id' not in request.session:
        return redirect('/')
    
    try:
        game_to_update = Game.objects.get(id=game_id)
    except Game.DoesNotExist:
        return redirect('/game/dashboard')
    
    if game_to_update.created_by.id == request.session['user_id']:
        errors =Game.objects.basic_validator(request.POST)
        
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect (f'/game/{game_id}/edit')
        else:
            Game.objects.update_game(request.POST , game_id)
            return redirect(f'/game/{game_id}')
        
    return redirect('/game/dashboard')

def favorite_game(request, game_id):
    if 'user_id' not in request.session:
        return redirect('/')
    
    try:
        game = Game.objects.get(id=game_id)
    except Game.DoesNotExist:
        return redirect('/game/dashboard')

    user = User.objects.get(id=request.session['user_id'])
    GameLike.objects.create(user = user , game = game , rate = request.POST.get('rate' , ''))
    
    # Redirect back to the page the user came from (either Main Page or Book Details)
    # If the referrer header is missing, safely default to the main '/books' page
    return redirect(request.META.get('HTTP_REFERER', '/game/dashboard'))



def unfavorite_game(request, game_id):
    if 'user_id' not in request.session:
        return redirect('/')
    
    try:
        game = Game.objects.get(id=game_id)
    except Game.DoesNotExist:
        return redirect('/game/dashboard')

    user = User.objects.get(id=request.session['user_id'])
    GameLike.objects.get(user = user , game =game).delete()
    
    return redirect(request.META.get('HTTP_REFERER', '/game/dashboard'))



def delete_game(request, game_id):
    if 'user_id' not in request.session:
        return redirect('/')
    try:
        game_to_delete = Game.objects.get(id=game_id)
    except Game.DoesNotExist:
        return redirect('/game/dashboard')
    
    if game_to_delete.created_by.id == request.session['user_id']:
        game_to_delete.delete()
        return redirect('/game/dashboard')
        
    return redirect('/game/dashboard')