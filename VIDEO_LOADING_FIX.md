# Django Movie Site - Video Loading Fix Guide

## Issues Fixed

### 1. **Video Player Configuration** ✓
- Added proper HTML5 video with multiple format support (mp4, webm)
- Added fallback download link for unsupported browsers
- Added fallback message when video file is not available
- Improved error handling

### 2. **Media Files Configuration** ✓
- Updated MEDIA_URL and MEDIA_ROOT settings
- Ensured proper path handling with Path objects
- Added STATIC_ROOT configuration for production

### 3. **URL Configuration** ✓
- Verified `static()` helper is imported and configured
- Confirmed MEDIA_URL and MEDIA_ROOT are correctly passed
- Media files will be served during development

## Verification Checklist

### Step 1: Check Media Directory Structure
```
movie_site/
├── media/
│   ├── movies/          # Your video files go here
│   ├── actors/          # Actor images
│   └── avatars/         # User avatars
├── static/
├── templates/
└── manage.py
```

### Step 2: Verify Settings
Check `movie_pr/settings.py`:
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
```

### Step 3: Verify URLs Configuration
Check `movie_pr/urls.py`:
```python
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # ... your patterns
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### Step 4: Upload Video Files
1. Go to Django Admin: http://127.0.0.1:8000/admin/
2. Add/Edit a Movie
3. Upload video file to "film" field
4. File will be saved to: `media/movies/filename.mp4`

### Step 5: Test the Setup
Run the test script:
```bash
python test_media_setup.py
```

Or test in Django shell:
```bash
python manage.py shell
>>> from movie_app.models import Movie
>>> movie = Movie.objects.first()
>>> print(movie.film.url)  # Should show: /media/movies/filename.mp4
>>> print(movie.film.path) # Should show: D:\...\media\movies\filename.mp4
```

### Step 6: Verify in Browser
1. Start server: `python manage.py runserver`
2. Navigate to: http://127.0.0.1:8000/film/1/
3. Video player should display and load
4. Check browser DevTools (F12) Network tab for any 404 errors

## Common Issues & Solutions

### Issue: Video Player Shows But No Video Plays
**Solution:**
1. Check if file exists: `media/movies/your_file.mp4`
2. Verify URL in browser Network tab (F12) - should be: `/media/movies/your_file.mp4`
3. Try different video format (mp4, webm, ogg)

### Issue: 404 Not Found for Video
**Solution:**
1. Ensure DEBUG=True in settings.py
2. Check MEDIA_URL and MEDIA_ROOT paths
3. Verify file is in the correct directory
4. Restart Django server after uploading files

### Issue: Permission Denied
**Solution:**
1. Check file permissions: `chmod 644 media/movies/*`
2. On Windows, ensure user has read permissions
3. Ensure media/ directory is readable

### Issue: Video Works Locally But Not on Production
**Solution:**
1. For production, configure a web server (Nginx, Apache)
2. Point static/media directories to your web server config
3. Use `python manage.py collectstatic` for static files
4. Configure X-Sendfile or equivalent for media serving

## Template Updates Made

### Before:
```html
<video class="video-player" controls preload="metadata">
    <source src="{{ movie.film.url }}" type="video/mp4">
    Your browser does not support the video tag.
</video>
```

### After:
```html
<div class="video-container">
    {% if movie.film %}
    <video class="video-player" controls preload="metadata">
        <source src="{{ movie.film.url }}" type="video/mp4">
        <source src="{{ movie.film.url }}" type="video/webm">
        <p>Your browser does not support the video tag. 
           <a href="{{ movie.film.url }}" download>Download the video instead</a>
        </p>
    </video>
    {% else %}
    <div class="bg-slate-700 rounded-lg p-12 text-center">
        <i class="fas fa-video text-6xl text-slate-500 mb-4 block"></i>
        <p class="text-slate-400">Video file not available for this movie</p>
    </div>
    {% endif %}
</div>
```

## Settings Updates Made

### Before:
```python
MEDIA_URL='/media/'
MEDIA_ROOT=BASE_DIR/'media'
```

### After:
```python
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

## Quick Start Commands

```bash
# 1. Ensure Django is running
python manage.py runserver

# 2. Test media configuration
python test_media_setup.py

# 3. Access admin to upload videos
# http://127.0.0.1:8000/admin/

# 4. View movie detail page
# http://127.0.0.1:8000/film/1/

# 5. Check Django shell
python manage.py shell
from movie_app.models import Movie
m = Movie.objects.first()
print(f"Video URL: {m.film.url}")
print(f"Video Path: {m.film.path}")
exit()
```

## Browser Testing

Open browser DevTools (F12) and check:
1. **Network tab**: Video request should return 200, not 404
2. **Console**: No errors about missing files
3. **Video tag**: Should show video controls
4. **File path**: `/media/movies/your_video.mp4`

## File Structure After Setup

```
media/
├── movies/
│   ├── movie_1.mp4
│   ├── movie_2.mp4
│   └── movie_3.webm
├── actors/
│   ├── 1_files/
│   ├── 2_files/
│   └── 3_files/
└── avatars/
    └── user_1.jpg
```

## Notes

- Videos should be in MP4 format (most compatible)
- Supported formats: MP4, WebM, Ogg
- Maximum file size depends on Django/server configuration
- For better performance, pre-encode videos to multiple formats
- Consider using CDN for video delivery on production

## Success Indicators

✓ Video URL loads correctly  
✓ Video player displays with controls  
✓ Video plays without errors  
✓ Works on mobile browsers  
✓ Responsive video container  
✓ Proper fallback messages shown
