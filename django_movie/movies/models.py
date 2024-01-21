from django.db import models
from datetime import date
from django.urls import reverse

class Category(models.Model):

    name = models.CharField("Category",max_length=150)
    description =models.TextField("Description")
    url = models.SlugField(max_length=160,unique=True)


    def __str__(self):
        return self.name
    class Meta:
        verbose_name ="Category"
        verbose_name_plural = "Category"

class Actor (models.Model):
    """Actors and directors"""
    name = models.CharField("name",max_length=100)
    age = models.PositiveSmallIntegerField("age",default=0)
    description = models.TextField("Description")
    image = models.ImageField("Image",upload_to="actors/")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse ('actor_detile', kwargs={"slug": self.name})

    class Meta:
        verbose_name= "Actors and directors"
        verbose_name_plural = "Actors and directors"

class Genre(models.Model):
    """Жанры"""
    name = models.CharField("Category", max_length=150)
    description = models.TextField("Description")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

class Movie(models.Model):
    """Фильм"""
    title = models.CharField("Название",max_length=100)
    tagline = models.CharField("Слоган",max_length=100,default='')
    description = models.TextField("Description")
    poster = models.ImageField("Постер", upload_to="movies/")
    year = models.PositiveSmallIntegerField("дата выхода", default=2019)
    country = models.CharField("страна",max_length=30)
    directors = models.ManyToManyField(Actor,verbose_name='режисер',related_name='film_director')
    actors = models.ManyToManyField(Actor,verbose_name='актеры',related_name='film_actor')
    genres = models.ManyToManyField(Genre,verbose_name="жанры")
    world_premiere = models.DateField("премьера в мире",default=date.today)
    budget = models.PositiveIntegerField("Бюджет",default=0,
                                         help_text="указывать сумму в долларах")
    fees_in_usa = models.PositiveIntegerField(
        "сборы в мире",default=0, help_text="указывать сумму в долларах"
    )
    category = models.ForeignKey(
        Category,verbose_name="Category",on_delete=models.SET_NULL,null=True
    )
    url = models.SlugField(max_length=130,unique=True)
    draft = models.BooleanField("Черновик",default=False)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('movie_detail', kwargs={"slug": self.url})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = "фильм"
        verbose_name_plural = "фильм"

class MovieShots(models.Model):
    """Кадры из фильма """
    title = models.CharField("Заголовок",max_length=100)
    description = models.TextField("Description")
    image = models.ImageField("Image",upload_to="movie_shots/")
    movie = models.ForeignKey(Movie,verbose_name="film",on_delete=models.CASCADE)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "кадры из фильма"
        verbose_name_plural = "кадры из фильма"


class RatingStar(models.Model):
    """звезда рейтинга"""
    value = models.SmallIntegerField("значение",default=0)


    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "звезда рейтинга"
        verbose_name_plural = "звезды рейтинга"
        ordering = ["-value"]


class Rating(models.Model):
    """Рейтинг"""
    ip = models.CharField("IP адрес",max_length=15)
    star = models.ForeignKey(RatingStar,on_delete=models.CASCADE,verbose_name="звезда")
    movie =models.ForeignKey(Movie,on_delete=models.CASCADE,verbose_name="фильм")

    def __str__(self):
        return f"{self.star}-{self.movie}"

    class Meta:
        verbose_name = " рейтинги"
        verbose_name_plural = "рейтинги"

class Reviews(models.Model):
    """Отзывы"""
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True
    )
    movie = models.ForeignKey(Movie, verbose_name="фильм", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.movie}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"












