from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLE_CHOICE = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin')
    ]

    role = models.CharField(
        choices=ROLE_CHOICE,
        default=USER,
        max_length=9
    )

    class Meta:
        ordering = ['-id']


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Categories(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(max_length=200)
    year = models.DateField()
    genres = models.ManyToManyField("Genre", related_name="titles")
    categories = models.ManyToManyField("Categories",
                                        related_name="titles")

    class Meta:
        ordering = ["year"]

    def __str__(self):
        return self.name
