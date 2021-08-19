from django.contrib.auth import REDIRECT_FIELD_NAME, authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import User, Snake, Trivia
from .forms import Questionform

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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def index(request):
    return render(request, "ColdBlooded/index.html")

def trivia(request):
    if request.method == 'POST':
        trivia = Trivia.objects.all()
        correct = 0
        incorrect = 0
        total = 0
        for t in trivia:
            if t.answer == request.POST.get(t.question):
                correct = correct + 1
            else:
                incorrect = incorrect + 1
            total = total + 1
        return render(request, 'ColdBlooded/')

    return render(request, "ColdBlooded/trivia.html", {
        "Trivia": Trivia.objects.all()
    })

def newtrivia(request):
    return render(request, "ColdBlooded/newtrivia.html")