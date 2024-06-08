# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
#в данный момент нам нужен дженерик ListView, который реализует вывод списка объектов модели, используя указанный шаблон. А вот какую модель, как и в какой шаблон выводить, мы должны указать сами.
from datetime import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product, ProductForm
from .filters import ProductFilter





class ProductsList(ListView):
    # Указываем модель, объекты которой мы будем выводить

    model = Product
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'name'
    #queryset = Product.objects.filter(price__lt = 50)

    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'products.html'# 'этот файл он видит блогадаря черз  settings.py TEMPLATES = [DIRS': [os.path.join(BASE_DIR, 'templates',)],
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'products'#взято с файла products.html {{ products }}
    paginate_by = 2  # вот так мы можем указать количество записей на странице

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = ProductFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs
# Метод get_context_data позволяет нам изменить набор данных,
    # который будет передан в шаблон.
    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        #context['filterset'] = self.filterset&nbsp;
        context['filterset'] = self.filterset;
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        context['next_sale'] = "Распродажа в среду!"
        #context['next_sale'] = None

        return context


class ProductDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Product
    # Используем другой шаблон — product.html
    template_name = 'product1.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'product'
def create_product(request):
    form = ProductForm()

    if request.method =='POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/products/')


    return render(request, 'product_edit.html', {'form': form})