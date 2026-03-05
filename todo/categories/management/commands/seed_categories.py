from django.core.management.base import BaseCommand
from todo.categories.models import Category

DEFAULT_CATEGORIES = [
    {'name': 'Hooman', 'icon': '👤'},
    {'name': 'Work',   'icon': '💼'},
    {'name': 'Food',   'icon': '🛒'},
]


class Command(BaseCommand):
    help = 'Seed default categories if they do not exist'


    def handle(self, *args, **kwargs):
        for data in DEFAULT_CATEGORIES:
            _, created = Category.objects.get_or_create(
                name=data['name'],
                defaults={'icon': data['icon']}
            )
            status = 'created' if created else 'already exists'
            self.stdout.write(f"  {data['name']}: {status}")
