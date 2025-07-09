import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from loguru import logger

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates a superuser if none exists'

    def handle(self, *args, **options):
        if User.objects.filter(is_superuser=True).count() == 0:
            username = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
            password = os.environ.get('ADMIN_PASSWORD', 'admin')
            phone = os.environ.get('ADMIN_PHONE', '1234567890')
            
            logger.info(f'Creating superuser with email {username}')
            
            admin = User.objects.create_superuser(
                email=username,
                phone=phone,
                password=password
            )
            
            admin.is_active = True
            admin.is_admin = True
            admin.save()
            
            self.stdout.write(self.style.SUCCESS(f'Superuser {username} created successfully'))
        else:
            self.stdout.write(self.style.SUCCESS('Superuser already exists'))