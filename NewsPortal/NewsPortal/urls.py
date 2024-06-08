"""
URL configuration for NewsPortal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from django.urls import include




urlpatterns = [
    # path — означает путь.
    # В данном случае путь ко всем товарам у нас останется пустым,
    # чуть позже станет ясно почему.
    # Т.к. наше объявленное представление является классом,
    # а Django ожидает функцию, нам надо представить этот класс в виде view.
    # Для этого вызываем метод as_view.
    path('admin/', admin.site.urls),

    path('pages/', include('django.contrib.flatpages.urls')),

    path('products/', include('simpleapp.urls')),
    # path('Posts/', include('news.urls')),
    path('Posts/', include('news.urls')),
    path('Postsid/', include('news.urls')),
    path('news/', include('news.urls')),
    path('newsid/', include('news.urls')),
    path('product_edit/', include('news.urls')),

    path('post_create/', include('news.urls')),
    path('', include('protect.urls')),
    path('sign/', include('sign.urls')),
    path('accounts/', include('allauth.urls')),
    #path('articles/', include('news.urls')),
    #path('news/post_created_email/', include('news.urls')),


]
