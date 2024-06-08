# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
# from django.views.generic import ListView
from django.http import HttpResponseRedirect
from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView, DetailView, CreateView,UpdateView,DeleteView
from .models import Author, Post, Category
from datetime import datetime
from .formss import PostForm
from .filters import PostFilter
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives, send_mail
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy



class PostsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    # ordering = 'title'
    ordering = '-time_in_post'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10  # вот так мы можем указать количество записей на странице


    # Метод get_context_data позволяет нам изменить набор данных,
    # который будет передан в шаблон.
    #метод для изображение времени в шаблоне
    def get_context_data(self, **kwargs):#get_context_data, позволяет нам получить дополнительные данные, которые будут переданы в шаблон.
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['news_count'] = self.get_queryset().count()###добавил показывает количество новостей
        context['time_now'] = datetime.utcnow()




        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        # context['next_sale'] = None
        return context

    # def get_queryset(self):
    #     # показываем только новости в порядке убывания даты публикации
    #     return Post.objects.filter(post_type='1').order_by('-input_time_in_post')
    #     # return Post.objects.all()
    # #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['news_count'] = self.get_queryset().count()
    #     return context






class PostsDetail(DetailView):#показывает по id ключу  по ссылке news\urls.py  path('<int:pk>', PostsDetail.as_view()),
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'posts.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'posts'

def create_post(request):
    if request.method =='POST':
        form = PostForm(request.POST)
        form.save()
        return HttpResponseRedirect('/Posts/')#перенапровленияе на главную страницу.

    form = PostForm()
    return render(request, 'news_edit.html', {'form': form})


class PostsDetail(DetailView):#показывает по id ключу  по ссылке news\urls.py  path('<int:pk>', PostsDetail.as_view()),
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'postsid.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'postsid'


class PostEdit(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'edit.html'
    success_url ='/news/'



class PostDelete(DeleteView):
    model = Post
    template_name = 'delete.html'
    context_object_name = 'post_delete'
    #success_url = reverse_lazy('posts_list')
    success_url ='/news/'







class NewsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    # ordering = 'title'
    ordering = 'name'
   # ordering = '-time_in_post'
    template_name = 'news.html'
    paginate_by = 2  # вот так мы можем указать количество записей на странице
    context_object_name = 'news'



    # Метод get_context_data позволяет нам изменить набор данных,
    # который будет передан в шаблон.
    #метод для изображение времени в шаблоне
    def get_context_data(self, **kwargs):#get_context_data, позволяет нам получить дополнительные данные, которые будут переданы в шаблон.
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['news_count'] = self.get_queryset().count()###добавил показывает количество новостей
        context['time_now'] = datetime.utcnow()


        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        # context['next_sale'] = None
        return context


class NewsidDetail(
    DetailView):  # показывает по id ключу  по ссылке news\urls.py  path('<int:pk>', PostsDetail.as_view()),
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'newsid.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'newsid'



class PostSearch(ListView):
    model = Post
    ordering = 'time_in_post'
    filterset_class = PostFilter
    template_name = 'search.html'
    context_object_name = 'search'
    paginate_by = 10


    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class CategoryList(ListView):
    model = Post
    template_name = 'categories.html'
    # template_name = 'category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(categories=self.category).order_by('-time_in_post')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context




@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    message = 'Вы подписались на категорию(views.py,subscribe.html) : '
    return render(request, 'subscribe.html', {'category': category, 'message': message})


@login_required
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.remove(user)
    message = 'Вы отписались от категории: '
    return render(request, 'subscribe.html', {'category': category, 'message': message})





def index(request):
    return HttpResponse("Привет. Вы на главной странице приложения NewsPortal!")






