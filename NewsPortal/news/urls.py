from django.urls import include, path
# Импортируем созданное нами представление
from .views import PostsList
from .views import PostsList, PostsDetail, NewsidDetail, create_post, PostEdit, PostDelete, PostSearch, CategoryList,subscribe
#CategoryListView, subscribe,#PostsOfCategoryList

urlpatterns = [
    # path — означает путь.
    # В данном случае путь ко всем товарам у нас останется пустым,
    # чуть позже станет ясно почему.
    # Т.к. наше объявленное представление является классом,
    # а Django ожидает функцию, нам надо представить этот класс в виде view.
    # Для этого вызываем метод as_view.
    path('', PostsList.as_view()),
    # path('',Post()),

    # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
    # int — указывает на то, что принимаются только целочисленные значения
    # path('<int:pk>',PostsDetail.as_view()),
    # path('<int:id>', PostsDetail.as_view()),
    # path('<int:pk>', PostsDetail1.as_view()),
    path('', PostsDetail.as_view(), name='posts_detail1'),
    path('<int:pk>/', PostsDetail.as_view()),
    path('news/<int:pk>/', PostsDetail.as_view(), name='posts_detail'),
    path('<int:pk>/', NewsidDetail.as_view()),
    path('create/', create_post, name='post_crete'),#новый пост
    path('<int:pk>/', PostsDetail.as_view()),
    path('<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),#редактирование
    # path('news/<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
    path('<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
    path('search/', PostSearch.as_view(), name='posts_search'),
    #path('category/', CategoryList.as_view(), name='categories'),
    #path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
    #path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
    path('category/<int:pk>/', CategoryList.as_view(), name='categories'),#http://127.0.0.1:8000/post_create/category/2/
    path('category/<int:pk>/subscribe', subscribe, name='subscribe'),
    path('category/', CategoryList.as_view(), name='categories'),
    path('<int:id_post>/subscribe/<int:id_category>/', subscribe, name='subscribe_category')



]
