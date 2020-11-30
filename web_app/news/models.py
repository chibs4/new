from django.db import models
from django.urls import reverse
from django.utils import timezone
import datetime


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    in_menu = models.BooleanField(default=False)
    order = models.IntegerField(default=1)
    number_of_articles = models.IntegerField(default=1)

    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse('category',args=(self.slug,))


class Author(models.Model):
    name = models.CharField(max_length=255,unique=True)
    avatar = models.ImageField(upload_to='images/avatars', default='/static/images/noava.png')
    bio = models.CharField(max_length=255,default='No bio')

    objects = models.Manager()

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    number_of_articles = models.IntegerField(default=1)

    objects = models.Manager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category',args=(self.slug,))


class Article(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    content = models.TextField()
    short_description = models.TextField(default='No description')
    main_image = models.CharField(max_length=500, default='/static/images/photos/image-8.jpg')
    pub_date = models.CharField(max_length=255,default=str(datetime.datetime.now()))
    categories = models.ManyToManyField(to=Category,default=None)
    tags = models.ManyToManyField(to=Tag,default=None)
    author = models.ForeignKey(to=Author, on_delete=models.CASCADE, related_name='author', default=1)
    views = models.IntegerField('views', default=0)


    objects = models.Manager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('post',args=(self.slug,))


class Comment(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(to=Article, on_delete=models.CASCADE, related_name='comments')

    objects = models.Manager()

    def __str__(self):
        return self.comment[:21]


class Mag(models.Model):
    name = models.CharField(max_length=255)
