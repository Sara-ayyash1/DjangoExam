from django.urls import path 
from . import views

urlpatterns = [
    path('dashboard' , views.index),
    path('add_game/' , views.create_game),
    path('<int:game_id>' , views.game_detail),
    path('<int:game_id>/edit' , views.edit_game),
    path('<int:game_id>/update' , views.update_game),
    path('<int:game_id>/delete' , views.delete_game),
    path('<int:game_id>/favorite' , views.favorite_game),
    path('<int:game_id>/unfavorite' , views.unfavorite_game),
]
