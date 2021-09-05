from django import forms
from django.forms.widgets import Widget
from .models import *
from django.contrib.auth.forms import UserCreationForm
 
class createuserform(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(createuserform, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
  
class Questionform(forms.ModelForm):
    class Meta:
        model=Trivia
        fields="__all__"
        #fields = [
        # 'question',
        # 'choice1', 
        # 'choice2',
        # 'choice3',
        # 'choice4',
        # 'answer']

class CreateForm(forms.ModelForm):
    class Meta:
        model = Snake
        fields = ['name', 'sciname', 'description', 'range', 'rangepic', 'picture', 'is_venomous']

