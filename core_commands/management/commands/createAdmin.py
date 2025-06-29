from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os


class Command(BaseCommand):
    help = 'Create an admin user using environment variables'

    def handle(self, *args, **options):
        User = get_user_model()
        
        # Get admin credentials from environment
        admin_username = os.getenv('ADMIN_USERNAME', 'admin')
        admin_email = os.getenv('ADMIN_EMAIL', 'admin@example.com')
        admin_password = os.getenv('ADMIN_PASSWORD', 'admin123')
        
        # Check if admin user already exists
        if User.objects.filter(username=admin_username).exists():
            self.stdout.write(
                self.style.WARNING(f'Admin user "{admin_username}" already exists.')
            )
            return
        
        # Create the admin user
        try:
            admin_user = User.objects.create_superuser(
                username=admin_username,
                email=admin_email,
                password=admin_password
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created admin user "{admin_username}"')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating admin user: {str(e)}')
            )