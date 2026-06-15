from django.db import models
from login_app.models import User
from datetime import date , datetime

# Create your models here.
class GameManager(models.Manager):
    def basic_validator(self , postData):
        errors ={}
        if len(postData.get('name' , '').strip()) <  2:
            errors['name'] = 'name is required!'
        if  postData.get('release_date', '')  and postData.get('release_date', '') >= str(date.today()):
            errors['release_date'] = 'release_date must be in the past!'
        if len(postData.get('description' , '').strip()) == 0:
            errors['description'] = 'description should not be blank!'
        return errors
    
    def create_game(self, postData):
        user_id = postData.get('user_id')
        try:
            creator = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise ValueError("User not found")

        new_game = self.create(
            name=postData.get('name', '').strip(),
            genre = postData.get('genre', '').strip(),
            release_date = datetime.strptime(postData.get('release_date', '') , '%Y-%m-%d'),
            description=postData.get('description', '').strip(),
            created_by=creator
        )
        
        return new_game
    
    def update_game(self, postData , game_id):
        user_id = postData.get('user_id')
        try:
            creator = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise ValueError("User not found")
        
        try:
            game = Game.objects.get(id=game_id)
        except Game.DoesNotExist:
            raise ValueError("Game not found")
        
        game.name=postData.get('name', '').strip()
        game.genre = postData.get('genre', '').strip()
        game.release_date = datetime.strptime(postData.get('release_date', '') , '%Y-%m-%d')
        game.description=postData.get('description', '').strip()
        game.created_by=creator

        game.save()
        return game


class Game(models.Model):
    name = models.CharField(max_length= 255)
    genre = models.CharField(max_length=255)
    release_date = models.DateField()
    description = models.TextField()
    players_how_likes = models.ManyToManyField(User , related_name="liked_games" , through='GameLike')
    created_by = models.ForeignKey(User , related_name='game_creator' , on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)
    objects = GameManager()

class GameLike(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    game = models.ForeignKey(Game , on_delete=models.CASCADE)
    rate = models.IntegerField()