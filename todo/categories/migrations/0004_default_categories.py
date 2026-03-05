from django.db import migrations


def create_default_categories(apps, schema_editor):
    Category = apps.get_model('categories', 'Category')
    defaults = [
        {'name': 'Hooman', 'icon': '👤'},
        {'name': 'Work', 'icon': '💼'},
        {'name': 'Food', 'icon': '🛒'},
    ]
    for data in defaults:
        Category.objects.get_or_create(name=data['name'], defaults={'icon': data['icon']})


def remove_default_categories(apps, schema_editor):
    Category = apps.get_model('categories', 'Category')
    Category.objects.filter(name__in=['Hooman', 'Work', 'Food']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0003_rename_emoji_to_icon'),
    ]

    operations = [
        migrations.RunPython(create_default_categories, remove_default_categories),
    ]
