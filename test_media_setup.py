"""
Test script to verify Django media file configuration and video loading
Run with: python manage.py shell < test_media_setup.py
Or: python test_media_setup.py
"""

import os
import sys
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_pr.settings')

try:
    import django
    django.setup()
except:
    pass

from django.conf import settings
from movie_app.models import Movie

print("=" * 60)
print("Django Media Configuration Test")
print("=" * 60)

# Test 1: Check MEDIA_URL and MEDIA_ROOT
print("\n✓ MEDIA Configuration:")
print(f"  MEDIA_URL: {settings.MEDIA_URL}")
print(f"  MEDIA_ROOT: {settings.MEDIA_ROOT}")

# Test 2: Check if media directory exists
media_path = Path(settings.MEDIA_ROOT)
if media_path.exists():
    print(f"\n✓ Media directory exists: {media_path}")
else:
    print(f"\n✗ Media directory NOT found: {media_path}")
    print(f"  Creating directory...")
    media_path.mkdir(parents=True, exist_ok=True)
    print(f"  ✓ Created: {media_path}")

# Test 3: Check if movies directory exists
movies_path = media_path / 'movies'
if movies_path.exists():
    print(f"✓ Movies directory exists: {movies_path}")
    movies = list(movies_path.glob('*'))
    if movies:
        print(f"  Files in movies directory: {len(movies)}")
        for movie_file in movies[:5]:
            print(f"    - {movie_file.name}")
    else:
        print(f"  No movie files found in directory")
else:
    print(f"✗ Movies directory NOT found: {movies_path}")
    print(f"  Creating directory...")
    movies_path.mkdir(parents=True, exist_ok=True)
    print(f"  ✓ Created: {movies_path}")

# Test 4: Check database movies and their film fields
print("\n✓ Database Movies:")
try:
    movies = Movie.objects.all()
    if movies.exists():
        print(f"  Total movies: {movies.count()}")
        for movie in movies[:5]:
            if movie.film:
                file_path = movie.film.path if hasattr(movie.film, 'path') else str(movie.film)
                file_url = movie.film.url if hasattr(movie.film, 'url') else f"{settings.MEDIA_URL}{movie.film}"
                file_exists = Path(file_path).exists() if hasattr(movie.film, 'path') else False
                status = "✓" if file_exists else "✗"
                print(f"  {status} {movie.id}. {movie.title}")
                print(f"      URL: {file_url}")
                print(f"      Path: {file_path}")
                if not file_exists:
                    print(f"      ⚠ File NOT found on disk!")
            else:
                print(f"  - {movie.id}. {movie.title} (No video file)")
    else:
        print("  No movies in database")
except Exception as e:
    print(f"  Error checking movies: {e}")

# Test 5: Check URL patterns
print("\n✓ URL Configuration:")
print(f"  STATIC_URL: {settings.STATIC_URL}")
print(f"  MEDIA_URL: {settings.MEDIA_URL}")
print(f"  DEBUG mode: {settings.DEBUG}")

# Test 6: Check if media is being served
print("\n✓ Media Serving Check:")
if settings.DEBUG:
    print("  ✓ DEBUG=True (media files will be served by Django)")
else:
    print("  ✗ DEBUG=False (you need to configure a web server to serve media)")

print("\n" + "=" * 60)
print("Configuration Summary:")
print("=" * 60)
print("""
To fix video loading issues:

1. Ensure video files are in: media/movies/
2. Check that movie.film field has the correct filename
3. Video URL should be: /media/movies/your_video_file.mp4
4. In Django shell:
   - from movie_app.models import Movie
   - m = Movie.objects.first()
   - print(m.film.url)  # Should show /media/movies/...
   
5. Test in browser by visiting:
   - Admin: http://127.0.0.1:8000/admin/movie_app/movie/
   - Detail page: http://127.0.0.1:8000/film/1/

If video still doesn't load:
- Check browser Network tab (F12) for 404 errors
- Verify file extension matches video type
- Check file permissions
- Try a different video format (mp4, webm, ogg)
""")
print("=" * 60)
