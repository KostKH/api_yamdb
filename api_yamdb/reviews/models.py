from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from django.utils.translation import gettext_lazy as _


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
    email = models.EmailField(_('email address'), blank=False, unique=True, max_length=254)
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    bio = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-id']
    
    def __str__(self):
        return self.username


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Categories(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    description = models.CharField(max_length=200, null=True, blank=True)
    genres = models.ManyToManyField("Genre",
                                    related_name="titles")
    categories = models.ForeignKey("Categories",
                                   on_delete=models.SET_NULL,
                                   related_name="titles",
                                   null=True)

    class Meta:
        ordering = ["year"]

    def __str__(self):
        return self.name


class Review(models.Model):
    author = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='reviews',
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
        "Title",
        blank=True,
        null=True,
        related_name="reviews",
        on_delete=models.SET_NULL)
    text = models.TextField(
        verbose_name='текст оценки',
        help_text='оцените произвидение')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review')
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text


class Comment(models.Model):
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
        related_name='comments',
        blank=True,
        null=True,
        on_delete=models.CASCADE)
    text = models.TextField(
        verbose_name='текст коментария',
        help_text='добавьте коментарий')


class UserCode(models.Model):
        user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_code'
        )
        code = models.CharField(max_length=5)

