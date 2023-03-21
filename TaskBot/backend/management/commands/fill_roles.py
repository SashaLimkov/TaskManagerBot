from django.core.management import BaseCommand

from backend.services.task_user import create_role


class Command(BaseCommand):
    help = "Fill first batch to DB"

    def handle(self, *args, **options):
        create_role("Исполнитель")
        create_role("Наблюдатель")
