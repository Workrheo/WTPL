from django.core.management.base import BaseCommand
from authapp.models import User
from django.core.management import call_command

class Command(BaseCommand):
    help = 'This will update your system to version 1.6.'

    def handle(self, *args, **options):
        # Run migrations
        self.stdout.write('Update initiating...')
        self.stdout.write('Running migrations...')
        call_command("makemigrations", interactive=False)
        call_command("migrate", interactive=False)
        self.stdout.write(self.style.SUCCESS('Migrations completed.'))

        
