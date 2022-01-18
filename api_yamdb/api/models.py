from django.db import models


class Category(models.Model):
    name = models.TextField('Название',
                            blank=False,
                            max_length=50)
    slug = models.SlugField('slug',
                            blank=False,
                            unique=True,
                            db_index=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.TextField('Название',
                            blank=False,
                            max_length=50)
    slug = models.SlugField('slug',
                            blank=False,
                            unique=True,
                            db_index=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.TextField(
        'Название',
        blank=False,
        max_length=50,
        db_index=True
    )
    year = models.IntegerField(blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles',
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        db_index=True,
        related_name='titles',
        verbose_name='Жанр'
    )
    description = models.CharField(
        'Описание',
        max_length=200,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name

