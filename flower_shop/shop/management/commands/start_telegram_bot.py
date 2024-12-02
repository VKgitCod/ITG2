# shop/management/commands/start_telegram_bot.py

from django.core.management.base import BaseCommand
from shop.telegram_bot import start_bot  # Импорт функции для запуска бота

class Command(BaseCommand):
    help = 'Запускает Telegram бота для уведомлений'

    def handle(self, *args, **options):
        self.stdout.write("Запуск Telegram бота...")
        start_bot()
