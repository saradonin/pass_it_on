from django.core.management.base import BaseCommand
from donations.models import Category, Institution
from accounts.models import User
from ._privatedata import create_categories, create_institutions


class Command(BaseCommand):
    help = 'Add institutions'
    
    def handle(self, *args, **options):
        if not Category.objects.exists():
            create_categories()
            self.stdout.write(self.style.SUCCESS("Categories created"))
            
        if not Institution.objects.exists():
            create_institutions()
            self.stdout.write(self.style.SUCCESS("Institutions created"))
            
        if not User.objects.exists():
            create_users()
            self.stdout.write(self.style.SUCCESS("Users added"))