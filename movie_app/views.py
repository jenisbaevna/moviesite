from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth import authenticate

from .models import Movie, Actors

def homepage(request):
    movies = Movie.objects.all()
    return render(request,'home.html',{'movies':movies})

def movie_detail(request, id):
    movie = get_object_or_404(Movie, id=id)
    return render(request, 'detail.html', {'movie': movie})

def actor_detail(request, slug):
    actor = get_object_or_404(Actors, slug=slug)
    movies = actor.movie_set.all()
    return render(request, 'actor_detail.html', {'actor': actor, 'movies': movies})
