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

        if not User.objects.filter(username='bsc_physics').exists():
            user=User.objects.create_user('bsc_pysics', 'bsc_physics@gmail.com', 'pass@123')
            user.save()

        if not User.objects.filter(username='bca').exists():
            user=User.objects.create_user('bca', 'bca@gmail.com', 'pass@123')
            user.save()

        if not User.objects.filter(username='bcom').exists():
            user=User.objects.create_user('bcom', 'bcom@gmail.com', 'pass@123')
            user.save()
