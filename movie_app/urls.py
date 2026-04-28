from django.urls import path
from .views import (
    homepage, 
    movie_detail, 
    actor_detail,
    register,
    login_view,
    logout_view,
    profile
)
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', homepage, name='home'),
    path('film/<int:id>/', movie_detail, name='movie_detail'),
    path('actor/<slug:slug>/', actor_detail, name='actor_detail'),
    
    # Authentication URLs
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile, name='profile'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)