from django.db import models
from login_app.models import User

# Create your models here.
class Manager(models.Manager):
    def basic_validator(self , postData):
        errors ={}
        if len(postData.get('title' , '').strip()) ==  0:
            errors['title'] = 'title is required!'
        if len(postData.get('description' , '').strip()) < 5:
            errors['description'] = 'description must be at least 5 characters!'
        return errors
    
class  (models.model):
    name = models.CharField(max_length= 255)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)
    objects = Manager()