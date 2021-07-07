from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Song
import logging

logger = logging.getLogger("django")

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
    songs = Song.objects.filter(user_id=request.user.id).values()

    if request.method == "POST":
        artist_name = request.POST.get("artist_name")
        song_name = request.POST.get("song_name")
        song_genre = request.POST.get("song_genre")

        if artist_name and song_name and song_genre:
            song = Song(
                artist_name=artist_name,
                song_name=song_name,
                song_genre=song_genre,
                user=request.user,
            )
            song.save()
            messages.success(request, "Musica salva com sucesso!")
            return render(request, "app/songs.html", {"songs": songs})

    return render(request, "app/songs.html", {"songs": songs})


@login_required(login_url="login")
def songsDelete(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    logger.info(song_id)
    if request.method == "POST":
        song.delete()
        messages.success(request, "Musica deletada com sucesso!")

    return redirect("songs")


@login_required(login_url="login")
def songsEdit(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    if song.user != request.user:
        messages.error(request, "Você não tem autorização para ver essa música!")
        return redirect("songs")

    elif request.method == "POST":
        song.artist_name = request.POST.get("artist_name")
        song.song_name = request.POST.get("song_name")
        song.song_genre = request.POST.get("song_genre")
        song.save()
        messages.success(request, "Musica alterada com sucesso!")
        return redirect("songs")

    return render(request, "app/edit_songs.html", {"song": song})


@login_required(login_url="login")
def trendingPage(request):
    return render(request, "app/trending.html")
