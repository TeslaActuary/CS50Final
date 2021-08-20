from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class Snake(models.Model):

    name = models.CharField(max_length=128, default='')
    sciname = models.CharField(max_length=128, default='', verbose_name="Science Name")
    description = models.TextField(default ='')
    picture = models.ImageField(blank=True)
    range = models.CharField(max_length=128,null=True)
    rangepic = models.URLField()
    funfacts = models.TextField(null=True, blank=True)
    is_venomous = models.BooleanField(default=False, verbose_name="Venomous?")

    def __str__(self):
        return self.name

class Trivia(models.Model):
    question = models.ImageField()
    choice1 = models.CharField(max_length=200,null=True)
    choice2 = models.CharField(max_length=200,null=True)
    choice3 = models.CharField(max_length=200,null=True)
    choice4 = models.CharField(max_length=200,null=True)
    answer = models.CharField(max_length=200,null=True)
    
    def __str__(self):
        return self.question