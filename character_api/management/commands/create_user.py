from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Create / overwrite a user / password."

    def add_arguments(self, parser):
        parser.add_argument("email", type=str, help="Email for user")
        parser.add_argument("password", type=str, help="password for user")

    def handle(self, *args, **options):
        email = options["email"]
        password = options["password"]
        if User.objects.filter(email=email).first() is not None:
            User.objects.get(email=email).delete()

        user = User(email=email, username=email)
        user.set_password(password)
        user.save()
        print(f"Created {email}")