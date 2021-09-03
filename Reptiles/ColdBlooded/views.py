from django.contrib.auth import REDIRECT_FIELD_NAME, authenticate, login, logout
from django.db import IntegrityError
from django.forms.models import ALL_FIELDS
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.urls.base import is_valid_path
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import User, Snake, Trivia
from .forms import Questionform, CreateForm, createuserform
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
        form = createuserform(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("index")
        messages.error(request, "Please check your entry. Invalid information.")
    form = createuserform()
    return render(request=request, template_name="ColdBlooded/register.html", context={"register_form":form})

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

@login_required(login_url='/accounts/login/')
def create(request):
    form = CreateForm()
    context = {
        'form': form
    }
    if request.method == 'POST':
        form = CreateForm(request.POST, request.FILES)
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

@login_required(login_url='/accounts/login/')
def edit(request, snake_name):
    content = Snake.objects.get(name=snake_name)
    form = CreateForm(initial={
        'name': content.name, 
        'sciname': content.sciname, 
        'description': content.description,
        'range': content.range,
        'picture': content.picture,
        'is_venomous': content.is_venomous
        })
    context = {
        'form': form
    }
    if request.method == "POST":
        form = CreateForm(request.POST, request.FILES, instance=content)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("detail", args=[content.id]))
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
