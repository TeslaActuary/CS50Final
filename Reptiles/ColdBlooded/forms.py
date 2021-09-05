from django import forms
from .models import *
#from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User
 
#class createuserform(UserCreationForm):
#    class Meta:
#        model=User
#        fields=['username','password'] 
 
class Questionform(forms.ModelForm):
    class Meta:
        model=Trivia
        #fields="__all__"
        fields = [
            'id',
            'question',
            'choice1', 
            'choice2',
            'choice3',
            'choice4',
            'answer']