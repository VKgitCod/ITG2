from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.product_catalog, name='catalog'),         # Главная страница
    path('register/', views.register, name='register'),      # Страница регистрации
    path('login/', views.user_login, name='login'),          # Страница входа
    path('logout/', LogoutView.as_view(), name='logout'),    # Страница выхода
    path('create_order/', views.create_order, name='create_order'), # Страница оформления заказа
]
