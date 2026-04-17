from django.db import models

from django.contrib.auth.models import AbstractUser

class CustomUSer(AbstractUser):
    phone_num=models.CharField(max_length=13,blank=True,null=True)
    avatar=models.ImageField(upload_to='avatars',blank=True,null=True)

class Actors(models.Model):
    name=models.CharField(max_length=50)
    surname=models.CharField(max_length=50)
    bio=models.TextField()
    birth_date=models.DateField()
    image=models.ImageField(upload_to='actors/',blank=True,null=True)
    def __str__(self):
        return self.name
class Genres(models.Model):
    genre=models.CharField(max_length=50)
    def __str__(self):
        return self.genre

class Country(models.Model):
    country=models.CharField(max_length=50)
    def __str__(self):
        return self.country
class Comments(models.Model):
    text=models.TextField()
    created_date=models.DateTimeField(auto_now_add=True)
    author=models.ForeignKey(CustomUSer,on_delete=models.CASCADE)
    def __str__(self):
        return self.text
class Languages(models.Model):
    language=models.CharField(max_length=50)

    def __str__(self):
        return self.language


class Movie(models.Model):
    title=models.CharField(max_length=255)
    year=models.DateField()
    image=models.ImageField(upload_to='movies/')
    desc=models.TextField()
    trailler=models.URLField()
    film=models.FileField()
    actor=models.ManyToManyField(Actors)
    countries=models.ManyToManyField(Country)
    comments=models.ManyToManyField(Comments,blank=True)
    languages=models.ManyToManyField(Languages)
    genres=models.ManyToManyField(Genres)
    def __str__(self):
        return self.title