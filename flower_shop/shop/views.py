from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
from .forms import UserRegisterForm, UserLoginForm, OrderForm
from .models import Product, Order
from .telegram_bot import send_order_to_telegram
from datetime import time

def register(request):
    """Регистрация нового пользователя."""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Создаем нового пользователя
            login(request, user)  # Входим под новым пользователем
            return redirect('catalog')  # Перенаправляем в каталог после регистрации
    else:
        form = UserRegisterForm()
    return render(request, 'shop/register.html', {'form': form})

def user_login(request):
    """Вход для зарегистрированного пользователя."""
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('catalog')
    else:
        form = UserLoginForm()
    return render(request, 'shop/login.html', {'form': form})

@login_required
def product_catalog(request):
    """Отображение каталога товаров."""
    products = Product.objects.all()
    return render(request, 'shop/catalog.html', {'products': products})

@login_required
def create_order(request):
    """Создание нового заказа и отправка уведомления в Telegram."""
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Проверяем, что заказ создается в рабочее время
            current_time = timezone.now().time()
            start_time, end_time = time(9, 0), time(18, 0)
            if start_time <= current_time <= end_time:
                # Сохраняем заказ
                order = form.save(commit=False)
                order.user = request.user
                order.save()
                form.save_m2m()  # Сохраняем связанные товары

                # Отправка информации о заказе администратору в Telegram
                send_order_to_telegram(order.id)

                return render(request, 'shop/success.html', {'order': order})
            else:
                # Сообщение об ошибке, если заказ делается вне рабочего времени
                error_message = "Заказы принимаются только с 9:00 до 18:00"
                return render(request, 'shop/create_order.html', {'form': form, 'error': error_message})
    else:
        form = OrderForm()
    return render(request, 'shop/create_order.html', {'form': form})
