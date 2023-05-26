from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.news_list, name='news_list'),
    path('<int:article_id>/', views.article_detail, name='article_detail'),
    path('create_articles/', views.create_articles, name='create_articles'),
    path('create/', views.create_articles, name='create_articles'),  # Маршрут для создания статей
    path('create_categories/', views.create_categories, name='create_categories'),
]
