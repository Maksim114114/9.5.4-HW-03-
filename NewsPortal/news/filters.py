from django import forms
from django_filters import FilterSet, ModelChoiceFilter, DateFilter
from django.db import models

from .models import Author, PostCategory, Post,Category

class PostFilter(FilterSet):
    date = DateFilter(field_name='time_in_post', lookup_expr='gt', widget=forms.DateInput(attrs={'type': 'date'}), label='Дата публикации')
    #title = ModelChoiceFilter(field_name='categories', queryset=Category, label='Категория(filters.py)', empty_label='Все категории',)
    title = ModelChoiceFilter(field_name='categories', queryset=Category.objects.all(), label='Категория(filters.py)',empty_label='Все категории', )
    author = ModelChoiceFilter(field_name='author', queryset=Author.objects.all(), label='Автор', empty_label='Все авторы')


    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'post_author': ['exact'],
            'categories': ['exact'],
           # 'event_choose':['exact']


        }

