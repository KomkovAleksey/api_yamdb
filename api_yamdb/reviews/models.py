from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from .validators import validate_year
from users.models import CustomUser


class Category(models.Model):
    """Category model."""

    name = models.CharField(max_length=256, verbose_name='Category')
    slug = models.SlugField(unique=True, verbose_name='Category page address')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Genre model."""

    name = models.CharField(max_length=256, verbose_name='Genre')
    slug = models.SlugField(unique=True, verbose_name='Genre page address')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Title model."""

    name = models.CharField(max_length=200, verbose_name='Title')
    year = models.IntegerField(
        verbose_name='Year',
        validators=[validate_year]
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='reviews',
        verbose_name='Category',
        null=True,
        blank=True,
    )
    description = models.TextField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Description'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='reviews',
        verbose_name='Genre',
        through='TitleGenre',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Title'
        verbose_name_plural = 'Titles'

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    """Model of connection between genres and titles."""

    title = models.ForeignKey(
        Title,
        verbose_name='Title',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    genre = models.ForeignKey(
        Genre,
        verbose_name='Genre',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Genre title'
        verbose_name_plural = 'Genres titles'

    def __str__(self):
        return f'{self.title} {self.genre}'


class Review(models.Model):
    """Review model."""

    text = models.TextField()
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='author'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='произведение'
    )
    score = models.IntegerField(
        verbose_name='score',
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(
        'Дата публикации отзыва',
        auto_now_add=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'reviews'
        verbose_name_plural = 'reviews'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            )
        ]


class Comment(models.Model):
    """Comment model."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='author'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'comments'
        verbose_name_plural = 'comments'

    def __str__(self):
        return self.text
