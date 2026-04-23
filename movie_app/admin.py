from django.contrib import admin
from .models import CustomUSer,Languages,Comments,Country,Movie,Actors,Genres
# Register your models here.


admin.site.register(Languages)
admin.site.register(Comments)
admin.site.register(Country)
admin.site.register(Movie)
admin.site.register(Actors)
admin.site.register(Genres)

class MoviesAdmin(admin.ModelAdmin):
    list_display=['title']
    search_fields=['title']
    list_filter=['film']