from django.core.management import BaseCommand

from bot.app import run_bot


class Command(BaseCommand):
    help = "Start Telegram Bot"

    def handle(self, *args, **options):
        run_bot()
