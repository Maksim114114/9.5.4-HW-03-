from django.db import models

from django import forms
from django.core.validators import MinValueValidator


# Товар для нашей витрины
class Product(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True, # названия товаров не должны повторяться
    )
    description = models.TextField()#description-описание (хлеб нарезной)
    quantity = models.IntegerField(
        validators=[MinValueValidator(0)],#quantity -количество( 1шт)
    )
    # поле категории будет ссылаться на модель категории
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='products', # все продукты в категории будут доступны через поле products
    )
    price = models.FloatField(
        validators=[MinValueValidator(0.0)],
    )
#Только что мы создали две простые модели. Одна из них представляет собой товар с полями, такими как имя, количество, описание и так далее. Другая — категорию товара, которая является первичным ключом к полю category у товара.

#Обратите внимание, что мы дополнительно указали методы __str__ у моделей. Django будет их использовать, когда потребуется где-то напечатать наш объект целиком. Например, в панели администратора или в темплейте. Вот как раз для вывода в HTML странице мы и указали, как должен выглядеть объект нашей модели.
    def __str__(self):
        return f'{self.name.title()}: {self.description[:20]}({self.price})'






# Категория, к которой будет привязываться товар
class Category(models.Model):
    # названия категорий тоже не должны повторяться
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name.title()

class ProductForm(forms.ModelForm):
   class Meta:
       model = Product
       fields = [
           'name',
           'description',
           'quantity',
           'category',
           'price',
       ]

