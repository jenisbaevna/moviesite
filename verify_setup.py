#!/usr/bin/env python
"""
Quick verification script for Django media setup
Run: python verify_setup.py
"""

import os
import sys
from pathlib import Path

print("\n" + "="*70)
print("DJANGO MEDIA SETUP VERIFICATION")
print("="*70 + "\n")

# Get project root
project_root = Path(__file__).parent
print(f"📁 Project Root: {project_root}\n")

# Check 1: Media Directory Structure
print("1️⃣  CHECKING MEDIA DIRECTORY STRUCTURE...")
media_dir = project_root / 'media'
required_dirs = ['movies', 'actors', 'avatars']

for dir_name in required_dirs:
    dir_path = media_dir / dir_name
    if dir_path.exists():
        file_count = len(list(dir_path.glob('*')))
        print(f"   ✓ {dir_name}/ exists ({file_count} files)")
    else:
        print(f"   ✗ {dir_name}/ missing - creating...")
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"   ✓ Created {dir_name}/")

# Check 2: Settings Configuration
print("\n2️⃣  CHECKING SETTINGS.PY CONFIGURATION...")
settings_file = project_root / 'movie_pr' / 'settings.py'
if settings_file.exists():
    with open(settings_file, 'r') as f:
        content = f.read()
    
    checks = {
        "MEDIA_URL = '/media/'": "MEDIA_URL configured",
        "MEDIA_ROOT = BASE_DIR / 'media'": "MEDIA_ROOT configured",
        "STATIC_URL = 'static/'": "STATIC_URL configured",
        "STATICFILES_DIRS": "STATICFILES_DIRS configured",
    }
    
    for check, description in checks.items():
        if check in content or check.replace(" = ", "=") in content:
            print(f"   ✓ {description}")
        else:
            print(f"   ✗ {description} - NOT FOUND")
else:
    print(f"   ✗ settings.py not found")

# Check 3: URL Configuration
print("\n3️⃣  CHECKING URLs.PY CONFIGURATION...")
urls_file = project_root / 'movie_pr' / 'urls.py'
if urls_file.exists():
    with open(urls_file, 'r') as f:
        content = f.read()
    
    if 'static(settings.MEDIA_URL' in content:
        print(f"   ✓ Media serving configured in urls.py")
    else:
        print(f"   ✗ Media serving NOT configured in urls.py")
else:
    print(f"   ✗ urls.py not found")

# Check 4: Template Configuration
print("\n4️⃣  CHECKING DETAIL.HTML TEMPLATE...")
detail_template = project_root / 'templates' / 'detail.html'
if detail_template.exists():
    with open(detail_template, 'r') as f:
        content = f.read()
    
    checks = {
        '{% if movie.film %}': "Conditional video check",
        '<video class="video-player"': "Video player element",
        '<source src="{{ movie.film.url }}"': "Video source tag",
        'type="video/mp4"': "MP4 format support",
        'type="video/webm"': "WebM format support",
        'download': "Download fallback link",
        '{% else %}': "Alternative content",
        'Video file not available': "Fallback message",
    }
    
    for check, description in checks.items():
        if check in content:
            print(f"   ✓ {description}")
        else:
            print(f"   ⚠ {description} - NOT FOUND (might be OK)")
else:
    print(f"   ✗ detail.html not found")

# Check 5: Database Status
print("\n5️⃣  CHECKING DATABASE MOVIES...")
try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_pr.settings')
    import django
    django.setup()
    
    from movie_app.models import Movie
    
    total_movies = Movie.objects.count()
    movies_with_video = Movie.objects.exclude(film='').count()
    
    print(f"   ✓ Total movies: {total_movies}")
    print(f"   ✓ Movies with video: {movies_with_video}")
    
    if movies_with_video > 0:
        sample = Movie.objects.exclude(film='').first()
        print(f"\n   Sample Movie: {sample.title}")
        print(f"   - Film URL: {sample.film.url}")
        
        # Check if file exists
        if sample.film:
            try:
                file_exists = os.path.exists(sample.film.path)
                status = "✓ EXISTS" if file_exists else "✗ NOT FOUND"
                print(f"   - File Path: {sample.film.path}")
                print(f"   - File Status: {status}")
            except:
                print(f"   - File: Unable to check")
    else:
        print(f"   ⚠ No movies with videos - upload one via admin!")
        
except Exception as e:
    print(f"   ✗ Database check failed: {e}")

# Check 6: Django Settings Summary
print("\n6️⃣  DJANGO CONFIGURATION SUMMARY...")
try:
    from django.conf import settings
    print(f"   DEBUG mode: {'✓ ON' if settings.DEBUG else '✗ OFF (media won't auto-serve)'}")
    print(f"   MEDIA_URL: {settings.MEDIA_URL}")
    print(f"   MEDIA_ROOT: {settings.MEDIA_ROOT}")
    print(f"   STATIC_URL: {settings.STATIC_URL}")
except Exception as e:
    print(f"   ✗ Could not read settings: {e}")

# Summary
print("\n" + "="*70)
print("NEXT STEPS:")
print("="*70)
print("""
1. Start Django server:
   python manage.py runserver

2. Upload a video file:
   - Go to: http://127.0.0.1:8000/admin/
   - Add a movie with video file
   
3. Test playback:
   - Visit: http://127.0.0.1:8000/film/1/
   - Video should play!

4. If video doesn't load:
   - Check browser DevTools (F12)
   - Look at Network tab
   - Video request should be 200, not 404
   - Check media/movies/ directory for file

5. Verify with Django shell:
   python manage.py shell
   from movie_app.models import Movie
   m = Movie.objects.first()
   print(m.film.url)
   print(m.film.path)
   exit()
""")
print("="*70 + "\n")
