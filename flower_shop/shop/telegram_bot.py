import os
import django
import telegram
from django.conf import settings
from .models import Order

# Установим настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flower_shop.settings')
django.setup()

# Инициализируем бота
bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)

def send_order_to_telegram(order_id):
    order = Order.objects.get(id=order_id)
    message = f"Новый заказ от {order.user.username}\nАдрес доставки: {order.delivery_address}\n"
    for product in order.products.all():
        message += f"- {product.name}: {product.price}\n"
    bot.send_message(chat_id=settings.TELEGRAM_ADMIN_ID, text=message)
    pass

def start_bot():
    """Функция для запуска бота, вызываемая командой Django"""
    # Здесь можно добавить обработку команд, если нужно
    # Например, bot.polling() или бот с webhook