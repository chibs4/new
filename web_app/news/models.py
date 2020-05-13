from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, default=1)
    in_menu = models.BooleanField(default=False)
    order = models.IntegerField(default=1)

    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse('category',args=(self.slug,))


class Author(models.Model):
    name = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to='images/avatars', default='images/avatars/noava.png')
    bio = models.CharField(max_length=255)

    objects = models.Manager()

    def __str__(self):
        return self.name


class Article(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    content = models.TextField()
    short_description = models.TextField()
    main_image = models.ImageField(upload_to='images')
    pub_date = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(to=Category)
    author = models.ForeignKey(to=Author, on_delete=models.CASCADE, related_name='author')
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


class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    articles = models.ManyToManyField(to=Article)

    objects = models.Manager()

    def __str__(self):
        return self.name


class Mag(models.Model):
    name = models.CharField(max_length=255)
