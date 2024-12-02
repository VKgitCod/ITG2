from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Order, Product


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Обязательно. Введите действительный адрес электронной почты.")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Имя пользователя", max_length=150)
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")


class OrderForm(forms.ModelForm):
    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Выберите товары"
    )
    delivery_address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        label="Адрес доставки",
        help_text="Введите адрес, по которому будет осуществляться доставка."
    )

    class Meta:
        model = Order
        fields = ['products', 'delivery_address']
