from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User
 
class createuserform(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model=User
        fields=['username', 'email', 'password1', 'password2']

        def save(self, commit=True):
            USER=super(createuserform, self).save(commit=False)
            user, email=self.cleaned_data['email']
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
        fields = ['name', 'sciname', 'description', 'range', 'picture', 'is_venomous']

        #widgets = {
        #    'name': forms.TextInput(attrs={'class': 'form-control'}),
        #    'sciname': forms.TextInput(attrs={'class': 'form-control', 'Placeholder': 'Enter the Scicence Name'}),
        #    'description': forms.Textarea(attrs={'class': 'form-control'}),
        #    'range': forms.TextInput(attrs={'class': 'form-control'}),
        #    'picture': forms.FileInput(attrs={'class': 'form-control-file'}),
        #    'is_venomous': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        #}

