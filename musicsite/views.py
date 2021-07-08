from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Song
import requests
import base64
import json
import os
import logging

logger = logging.getLogger("views")

# from django.http import HttpResponse

countries = {
    "Global": "37i9dQZEVXbMDoHDwVN2tF",
    "United States": "37i9dQZEVXbLRQDuF5jeBp",
    "Brazil": "37i9dQZEVXbMXbN3EUUhlg",
    "Japan": "37i9dQZEVXbKXQ4mDTEBXq",
    "Spain": "37i9dQZEVXbNFJfN1Vw8d9",
    "Argentina": "37i9dQZEVXbMMy2roB9myp",
    "Mexico": "37i9dQZEVXbO3qyFxbkOE1",
    "France": "37i9dQZEVXbIPWwFssbupI",
    "Italy": "37i9dQZEVXbIQnj7RRhdSX",
    "Germany": "37i9dQZEVXbJiZcmkrIHGU",
    "Indonesia": "37i9dQZEVXbObFQZ3JLcXt",
    "United Kingdom": "37i9dQZEVXbLnolsZ8PSNw",
    "Sweden": "37i9dQZEVXbLoATJ81JYXz",
    "South Korea": "37i9dQZEVXbNxXF4SkHj9F",
    "Netherlands": "37i9dQZEVXbKCF6dqVpDkS",
    "Portugal": "37i9dQZEVXbKyJS56d1pgi",
    "Chile": "37i9dQZEVXbL0GavIqMTeb",
    "Colombia": "37i9dQZEVXbOa2lmxNORXQ",
    "Norway": "37i9dQZEVXbJvfa0Yxg7E7",
    "Philippines": "37i9dQZEVXbNBz9cRCSFkY",
    "Paraguay": "37i9dQZEVXbNOUPGj7tW6T",
    "Turkey": "37i9dQZEVXbIVYVBNw9D5K",
    "Australia": "37i9dQZEVXbJPcfkRz0wJ0",
    "Peru": "37i9dQZEVXbJfdy5b0KP7W",
    "Denmark": "37i9dQZEVXbL3J0k32lWnN",
    "Finland": "37i9dQZEVXbMxcczTSoGwZ",
    "Canada": "37i9dQZEVXbKj23U1GF4IR",
    "Poland": "37i9dQZEVXbN6itCcaL3Tt",
    "Russia": "37i9dQZEVXbL8l7ra5vVdB",
    "Ireland": "37i9dQZEVXbKM896FDX8L1",
}


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
    context = {"countries": list(countries.keys())}

    if request.method == "POST":
        country = request.POST.get("country_name")
        if country == "default":
            messages.error(request, "Por favor, escolha um país")
            return redirect("trending")
        context["country"] = country

        token = getSpotifyToken()
        if not token:
            messages.error(request, "Erro ao comunicar com o Spotify")
            return redirect("trending")

        playlist = getPlaylist(token, country)
        if playlist:
            context["playlist"] = playlist
        else:
            messages.error(request, "Erro ao comunicar com o Spotify")
            return redirect("trending")

    return render(request, "app/trending.html", context)


def getSpotifyToken():
    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={"grant_type": "client_credentials"},
        headers={
            "Authorization": "Basic "
            + base64.b64encode(
                f"{os.getenv('CLIENT_ID')}:{os.getenv('CLIENT_SECRET')}".encode("ascii")
            ).decode("ascii")
        },
    )
    if not response:
        return False

    return json.loads(response.content)["access_token"]


def getPlaylist(token, country):
    playlist_id = countries[country]
    response = requests.get(
        f"https://api.spotify.com/v1/playlists/{playlist_id}",
        headers={"Authorization": "Bearer " + token},
    )

    if not response:
        return False

    return json.loads(response.content)["tracks"]["items"]
