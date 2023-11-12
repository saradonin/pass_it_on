from donations.models import Category, Institution
from accounts.models import User
import random

CATEGORY_LIST = ['artefakty', 'jedzenie',
                 'odzież', 'książki', 'zabawki', 'złoto']


def create_categories():
    for category in CATEGORY_LIST:
        if not Category.objects.filter(name=category).exists():
            Category.objects.create(name=category)


def create_institutions():
    for i in range(2):
        type = random.randint(1, 3)
        if type == 1:
            name = f"Fundacja {i+1}"
        elif type == 2:
            name = f"Organizacja {i+1}"
        elif type == 3:
            name = f"Zbiórka {i+1}"
        description = f"Przykładowy opis organizacji: {name}"
            
        institution = Institution.objects.create(name=name, description=description, type=type)
        
        for _ in range(random.randint(1, 3)):
            category = Category.objects.order_by('?')[0]
            institution.categories.add(category)


def create_users():
    User.objects.create_superuser(username='admin', email='admin@oddam.org', password='admin')
    for i in range(2):
        username = f"user{i+1}"
        email = f"user{i+1}@oddam.org"
        User.objects.create_user(username=username, email=email, password='password123')
