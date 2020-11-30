from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator


from .models import Article, Category, Tag, Comment, Author
from .forms import CommentForm


class IndexListView(ListView):
    template_name = 'news/index.html'
    model = Article
    ordering = '-pub_date'
    paginate_by = 5

@method_decorator(csrf_protect, name='dispatch')
class PostDetailedView(DetailView):
    template_name = 'news/post.html'
    model = Article
    slug_url_kwarg = 'slug'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.views += 1
        self.object.save(update_fields=['views'])
        context = self.get_context_data()
        return self.render_to_response(context)


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
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['slug'] = Category.objects.get(slug=self.slug)
        except:
            context['slug'] = Tag.objects.get(slug=self.slug)
        if context:
            return context
        else:
            context['slug'] = Author.objects.get(name=self.slug)
            return context

    def get_queryset(self):
        self.slug = self.kwargs.get('slug')
        qs = super().get_queryset()
        qs = qs.filter(categories__slug=self.slug)
        if not qs.exists():
            qs = super().get_queryset()
            qs = qs.filter(author__name=self.slug)
            if not qs.exists():
                qs = super().get_queryset()
                qs = qs.filter(tags__slug=self.slug)
                return qs
            return qs
        else:
            return qs


class RobotsView(TemplateView):
    template_name = 'news/robots.html'
    content_type = 'text/plain'


class ContactView(TemplateView):
    template_name = 'news/contact-us.html'

class SearchListView(ListView):
    template_name = 'news/search.html'
    model = Article
    paginate_by = 5


    def get_queryset(self):
        query = self.request.GET.get('q')
        vector = SearchVector('name', weight='A') + SearchVector('content', weight='C') + SearchVector('categories__name', weight='B')
        query = SearchQuery(query)
        results = Article.objects.annotate(rank=SearchRank(vector,query)).filter(rank__gte=0.2).order_by('rank')
        return results






#
# def header_handler(request):
#     context={}
#     return render(request, 'chunks/header.html',context)
