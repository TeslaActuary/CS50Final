from django.contrib.auth import REDIRECT_FIELD_NAME, authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import User, Snake, Trivia
from .forms import Questionform, CreateForm

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
            return render(request, "ColdBlooded//login.html", {
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
            return render(request, "ColdBlooded//register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "ColdBlooded//register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "ColdBlooded//register.html")

def index(request):
    return render(request, "ColdBlooded/index.html")

def list(request, venomous):
    snakes= Snake.objects.filter(is_venomous=venomous)
    return render(request, "ColdBlooded/list.html",{
        "snakes": snakes
    })

def detail(request, snake_id):
    snake = Snake.objects.get(pk=snake_id)
    return render(request, "ColdBlooded/detail.html", {
        "snake": snake,
    })

def trivia(request):
    return render(request, "ColdBlooded/trivia.html")

def newtrivia(request):
    return render(request, "ColdBlooded/newtrivia.html")

def create(request):
    form = CreateForm()
    context = {
        'form': form
    }
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid():           
            try:
                snake_name = form.cleaned_data["name"]
                snake = Snake.objects.get(name=snake_name)  
                #new = form.save(commit=False)
                return render(request, "ColdBlooded/entry.html", {
                    'form': form, 
                    'message': "This entry already exists."
                    })
            except Snake.DoesNotExist:
                form.save()
                return HttpResponseRedirect(reverse("detail", args=[snake.id]))
        else:
            return render(request, "ColdBlooded/entry.html", context)
    else:
        return render(request, "ColdBlooded/entry.html", context)

def edit(request, snake_name):
    content = Snake.objects.get(name=snake_name)
    form = CreateForm(initial={
        'name': content.name, 
        'sciname': content.sciname, 
        'description': content.description,
        'picture': content.picture,
        'is_venomous': content.is_venomous
        })
    context = {
        'form': form
    }
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "ColdBlooded/entry.html", context)
    else:
        return render(request, "ColdBlooded/entry.html", context)

def search(request):
    if request.method == "GET":
        search = request.GET.get('search')
        results = Snake.objects.filter(name__contains=search)
        print(search)
        print(results)
        return render(request, "ColdBlooded/search.html", {
            'search': search,
            'results':results
            })
    else:
        return render(request, "ColdBlooded/search.html", {})
