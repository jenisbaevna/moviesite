from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Movie, Actors
from .forms import CommentForm, RegistrationForm, LoginForm


def homepage(request):
    movies = Movie.objects.all()
    query = request.GET.get('q')

    if query:
        movies = movies.filter(
            Q(title__icontains=query) |
            Q(desc__icontains=query) |
            Q(actor__name__icontains=query) |
            Q(countries__country__icontains=query) |
            Q(genres__genre__icontains=query) |
            Q(languages__language__icontains=query) |
            Q(year__icontains=query)
        ).distinct()

    return render(request, 'home.html', {'movies': movies})


def movie_detail(request, id):
    movie = get_object_or_404(Movie, id=id)
    comments = movie.comments.all()

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.movie = movie
                comment.author = request.user
                comment.save()
                messages.success(request, 'Comment posted successfully!')
                return redirect('movie_detail', id=id)
        else:
            messages.error(request, 'You must be logged in to comment.')
            return redirect('login')
    else:
        form = CommentForm()

    return render(request, 'detail.html', {
        'movie': movie,
        'comments': comments,
        'form': form
    })


def actor_detail(request, slug):
    actor = get_object_or_404(Actors, slug=slug)
    movies = actor.movie_set.all()
    return render(request, 'actor_detail.html', {
        'actor': actor,
        'movies': movies
    })


# ===================== AUTHENTICATION VIEWS =====================

def register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Auto-login the user after registration
            login(request, user)
            messages.success(request, f'Welcome {user.first_name}! Your account has been created.')
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Authenticate using email as username
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required(login_url='login')
def profile(request):
    """User profile view - only for authenticated users"""
    return render(request, 'profile.html', {'user': request.user})