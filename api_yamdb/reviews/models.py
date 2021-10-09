from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from .managers import CustomUserManager
from django.utils.translation import ugettext_lazy as _


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
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    bio = models.CharField(max_length=10, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    password = None
    last_login = None
    is_staff = None
    is_superuser = None
    is_active = None
    date_joined = None
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

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
    year = models.IntegerField()
    genres = models.ManyToManyField("Genre", related_name="titles")
    categories = models.ManyToManyField("Categories",
                                        related_name="titles")

    class Meta:
        ordering = ["year"]

    def __str__(self):
        return self.name

class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='author',
        null=False)
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True)
    score = models.PositiveIntegerField(
        default=10,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='оценка')
    title = models.ForeignKey(
        "Titles",
        blank=True,
        null=True,
        on_delete=models.SET_NULL)
    text = models.TextField(
        verbose_name='текст оценки',
        help_text='оцените произвидение')


class Comments(models.Model):
    author = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        verbose_name='author',
        null=False)
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True)
    review = models.ForeignKey(
        "Review",
        blank=True,
        null=True,
        on_delete=models.CASCADE)
    text = models.TextField(
        verbose_name='текст коментария',
        help_text='добавьте коментарий')

