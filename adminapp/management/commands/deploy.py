from django.core.management.base import BaseCommand
from authapp.models import User
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Create a superuser with a specified password, run migrations, and collect static files'

    def handle(self, *args, **options):
        # Run migrations
        self.stdout.write('Running migrations...')
        call_command("makemigrations", interactive=False)
        call_command("migrate", interactive=False)
        self.stdout.write(self.style.SUCCESS('Migrations completed.'))
        
        # Define superuser information
        username = 'admin'
        email = 'admin@gmail.com'
        password = '123456'

        # Create a superuser if it doesn't already exist
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_superuser(username, email, password)
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created successfully.'))
        else:
            self.stdout.write(self.style.ERROR(f'Superuser with username "{username}" already exists.'))

        
