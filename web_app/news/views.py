from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.detail import SingleObjectMixin
from django.contrib import messages
from django.shortcuts import render
from .models import Article, Category, Tag, Comment, Author
from .forms import CommentForm


class IndexListView(ListView):
    template_name = 'news/index.html'
    model = Article
    ordering = '-pub_date'
    paginate_by = 1


# def post_handler(request, slug):
#     article = Article.objects.get(slug=slug)
#     context = {'article': article}
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             data = form.cleaned_data
#             data['article'] = article
#             Comment.objects.create(**data)
#         else:
#             messages.add_message(request, messages.INFO, 'Error in FORM fields')
#     else:
#         form = CommentForm()
#     context['form'] = form
#     return render(request, 'news/post.html', context)


class PostDetailedView(DetailView):
    template_name = 'news/post.html'
    model = Article
    slug_url_kwarg = 'slug'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data['article'] = self.object
            Comment.objects.create(**data)
            form = CommentForm()

        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)


class CategoryListView(ListView):
    template_name = 'news/category.html'
    model = Article
    ordering = '-pub_date'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['slug'] = Category.objects.get(slug=self.slug)
        except:
            context['slug'] = Author.objects.get(name=self.slug)
        return context

    def get_queryset(self):
        self.slug = self.kwargs.get('slug')
        qs = super().get_queryset()
        qs = qs.filter(categories__slug=self.slug)
        if not qs.exists():
            qs = super().get_queryset()
            qs = qs.filter(author__name=self.slug)
            return qs
        else:
            return qs


class Error404View(TemplateView):
    template_name = 'news/error-404.html'


class RobotsView(TemplateView):
    template_name = 'news/robots.html'
    content_type = 'text/plain'


class PhotoGalleryView(TemplateView):
    template_name = 'photo-gallery.html'


class ContactView(TemplateView):
    template_name = 'news/contact-us.html'

#
# def header_handler(request):
#     context={}
#     return render(request, 'chunks/header.html',context)
