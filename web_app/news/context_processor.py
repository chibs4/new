from django.db.models import Count, Sum
from random import random
from .models import Category, Tag, Article
from django.utils import timezone


def menu_categories(request):
    cat_list = Category.objects.annotate \
                   (count=Count('article')).exclude(in_menu=True).order_by('-count')[:5]

    return {'cats_list': cat_list}


def tags(request):
    tags_list = Tag.objects.all()
    random_tags = sorted(tags_list[:10], key=lambda x: random())
    return {'random_tags': random_tags}


def popular_articles(request):
    popular_list = Article.objects.filter(
        pub_date__range=[timezone.now() - timezone.timedelta(3), timezone.now()]).annotate(sum=Sum('views')).order_by(
        '-sum')[:4]
    return {'popular_list': popular_list}
