from django.contrib import admin
from .models import Category, Product

#Не забываем зарегистрировать модели, иначе мы не увидим их в админке.
#simpleapp/admin.py
admin.site.register(Category)
admin.site.register(Product)