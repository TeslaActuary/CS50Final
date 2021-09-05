from django.contrib.auth import REDIRECT_FIELD_NAME, authenticate, login, logout
from django.db import IntegrityError
from django.forms.models import ALL_FIELDS
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.urls.base import is_valid_path

from .models import User, Snake, Trivia
from .forms import Questionform
from . import utils

# Create your views here.
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "ColdBlooded/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "ColdBlooded/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "ColdBlooded/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "ColdBlooded/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "ColdBlooded/register.html")

def index(request):
    return render(request, "ColdBlooded/index.html")

#initialize trivia outside of trivia request
trivia = utils.quiz_list(3)

def trivia(request):

    global count, trivia

    if request.method == 'POST':
        correct = 0
        incorrect = 0
        total = 0
        correct_answers = []
        incorrect_answers = []
        for t in trivia:

            if t.answer == request.POST.get(t.question):
                correct = correct + 1
                correct_answers.append(t.answer)
                # store correct answer question id's in array

            else:
                incorrect = incorrect + 1
                #store incorrect answer question id's in array
                incorrect_answers.append(t.answer)
            total = total + 1
        result = correct/total

        return render(request, 'ColdBlooded/result.html', {
            "Incorrect": incorrect,
            "Correct": correct,
            "Total": total,
            "Incorrect_answers": incorrect_answers, 
            "Correct_answers": correct_answers,
            "Trivia": trivia,
            "Result": result,
        })

    else:
        trivia = utils.quiz_list(3)
        return render(request, "ColdBlooded/trivia.html", {
            "Trivia": trivia
        })

def newtrivia(request):
    form=Questionform()
    if(request.method=='POST'):
        form=Questionform(request.POST, request.FILES)
        if(form.is_valid()):
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "ColdBlooded/newtrivia.html", {
            'form': form
            })
    else:
        return render(request, "ColdBlooded/newtrivia.html", {
            'form': form
        })