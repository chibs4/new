from django.db.models import Count, Sum
from random import random
from .models import Category, Tag, Article
from django.utils import timezone
from django.db.models import Max


def menu_categories(request):
    cat_list = Category.objects.annotate \
                   (count=Count('article')).exclude(in_menu=True).order_by('-count')[:5]

    return {'cats_list': cat_list}


def tags(request):
    tags_list = Tag.objects.all()
    random_tags = sorted(tags_list[:10], key=lambda x: random())
    return {'random_tags': random_tags}

def random_images(request):
    article_list = Article.objects.all()
    random_images = sorted(article_list[:5], key=lambda x: random())
    return {'random_images': random_images}


def popular_articles(request):
    popular_list = Article.objects.annotate(sum=Sum('views')).order_by(
        '-sum')[:4]
    return {'popular_list': popular_list}


# def random_images(request):
#     rand_images = []
#     for i in range(0,5):
#         max_id = Article.objects.all().aggregate(max_id=Max("id"))['max_id']
#         while True:
#             pk = random.randint(1, max_id)
#             article = Article.objects.filter(pk=pk).first()
#             if article:
#                 rand_images.append(article)
#                 break
#     return rand_images

