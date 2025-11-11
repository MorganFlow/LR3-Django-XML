import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from myapp.models import Tour

print("Перенос данных из SQLite в PostgreSQL...")

sqlite_tours = Tour.objects.using('sqlite').all()
for tour in sqlite_tours:
    new_tour = Tour(
        name=tour.name,
        description=tour.description,
        duration=tour.duration,
        price=tour.price,
        difficulty=tour.difficulty
    )
    new_tour.save(using='default')

print(f"Перенесено {sqlite_tours.count()} записей.")