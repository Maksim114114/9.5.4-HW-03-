from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
#from NewsPortal.models import *
from django.urls import reverse
from django.core.cache import cache
from datetime import datetime
from .utils import *
from django.core.validators import MinValueValidator
#from news.models import *




class Author(models.Model):
    author_user = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.IntegerField(default=0, null=True)



    def update_rating(self):
        post_rating = self.post_set.aggregate(post_rating=Sum('post_rating'))

        p_rat = 0
        p_rat += post_rating.get('post_rating')

        comment_rat = self.author_user.comment_set.aggregate(comment_rating=Sum('comment_rating'))
        c_rat = 0
        c_rat += comment_rat.get('comment_rating')

        self.author_rating = p_rat * 3 + c_rat
        self.save()



class Category(models.Model):
   #name_category = models.CharField(max_length=255, unique=True)
   objects = None
   name = models.CharField(max_length=128, unique=True)  # максмиальная длина 128 знаков, уникальное поле
   subscribers = models.ManyToManyField(User, blank=True, related_name='categories')
   #category = models.CharField(max_length=128, unique=True)  # максмиальная длина 128 знаков, уникальное поле

   def __str__(self):
       return self.name


   # def __str__(self):
   #     return self.category


class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    in_category = models.ForeignKey(Category, on_delete=models.CASCADE)




class Post(models.Model):
    news = "NS"
    papers = "PP"
    event_choose = [(news, "Новость"), (papers, "Статья")]
    post_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, through=PostCategory)
    time_in_post = models.DateTimeField(auto_now_add=True)
    event = models.CharField(choices=event_choose, max_length=2)
    title = models.CharField(max_length=199)
    post_text = models.TextField()
    post_rating = models.IntegerField(default=0)

    def like_post(self):
        self.post_rating += 1
        self.save()

    def dislike_post(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return self.post_text[:125:] + "..."

    def __str__(self):
        return f'{self.title.title()}:{self.post_text[::]}'



class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_in_comment = models.DateTimeField(auto_now_add=True)
    comment_text = models.TextField(unique=True)

    comment_rating = models.IntegerField(default=0)

    def like_comment(self):
        self.comment_rating += 1
        self.save()

    def dislike_comment(self):
        self.comment_rating -= 1
        self.save()


