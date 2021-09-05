from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class Snake(models.Model):

    name = models.CharField(max_length=128, default='')
    sciname = models.CharField(max_length=128, default='', verbose_name="scientific name")
    description = models.TextField(default ='')
    picture = models.ImageField()
    range = models.CharField(max_length=128,null=True)
    rangepic = models.URLField(blank=True, verbose_name="Range Map (URL to range map)")
    funfacts = models.TextField(null=True, blank=True)
    is_venomous = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.sciname}"

class Trivia(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.ImageField()
    choice1 = models.CharField(max_length=200,null=True)
    choice2 = models.CharField(max_length=200,null=True)
    choice3 = models.CharField(max_length=200,null=True)
    choice4 = models.CharField(max_length=200,null=True)
    answer = models.CharField(max_length=200,null=True)
    
    def __int__(self):
        return self.answer