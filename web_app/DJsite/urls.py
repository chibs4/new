"""DJsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.views.decorators.cache import cache_page
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap,index
from django.conf import settings
from news.views import PhotoGalleryView, Error404View, RobotsView, CategoryListView, \
    IndexListView, PostDetailedView,SearchListView
from news import sitemaps



urlpatterns = [
                  path('', cache_page(60*60)(IndexListView.as_view()), name='homepage'),
                  path('photo-gallery/', cache_page(60*60)(PhotoGalleryView.as_view())),
                  path('post/<slug>/', (PostDetailedView.as_view()), name='post'),
                  path('error-404/', Error404View.as_view()),
                  path('search/', cache_page(60*60)(SearchListView.as_view()), name='search'),

                  path('summernote/', include('django_summernote.urls')),
                  path('admin/', admin.site.urls),
                  path('robots.txt/', RobotsView.as_view()),
                  path('sitemap.xml', cache_page(86400)(index), {'sitemaps': sitemaps.sitemaps}),
                  path('sitemap-<section>.xml', cache_page(86400)(sitemap), {'sitemaps': sitemaps.sitemaps},
                       name='django.contrib.sitemaps.views.sitemap'),
                  path('<slug>/', cache_page(60*60)(CategoryListView.as_view()), name='category'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
