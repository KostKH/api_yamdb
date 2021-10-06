from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
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
