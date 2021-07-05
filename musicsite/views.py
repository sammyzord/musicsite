from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# from django.http import HttpResponse


def index(request):
    return render(request, "homepage.html")


def registerPage(request):
    if request.user.is_authenticated:
        return redirect("index")

    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuário cadastrado com sucesso!")
            return redirect("login")

    context = {"form": form}
    return render(request, "register.html", context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            messages.success(request, "Bem vindo, %s!" % user)
            login(request, user)
            return redirect("index")
        else:
            messages.error(request, "Usuário ou senha inválidos.")
            return render(request, "login.html")

    return render(request, "login.html")


def logoutUser(request):
    logout(request)
    return redirect("login")


@login_required(login_url="login")
def songsPage(request):
    return render(request, "app/songs.html")


@login_required(login_url="login")
def trendingPage(request):
    return render(request, "app/trending.html")
