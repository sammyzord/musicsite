from django.shortcuts import render

# from django.http import HttpResponse


def index(request):
    return render(request, "homepage.html")


def songs(request):
    return render(request, "app/songs.html")


def trending(request):
    return render(request, "app/trending.html")
