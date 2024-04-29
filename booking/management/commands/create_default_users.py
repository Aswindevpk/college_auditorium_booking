from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Creates initial users for the project'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@gmail.com', 'pass')
        if not User.objects.filter(username='sjcadmin').exists():
            user=User.objects.create_user('sjcadmin', 'sjcadmin@gmail.com', 'pass@123')
            user.is_staff=True
            user.save()
        if not User.objects.filter(username='sjcmain').exists():
            user=User.objects.create_user('sjcmain', 'sjcmain@gmail.com', 'pass@123')
            user.is_staff=True
            user.save()
