from django.utils.crypto import get_random_string
from django.core.management.base import BaseCommand

#generate a secret key for the project
class Command(BaseCommand):
    def handle(self, *args, **options):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        with open("xbikeframework/settings.py", "a") as f:
            f.write("\n# SECURITY WARNING: keep the secret key used in production secret!\nSECRET_KEY = '"+get_random_string(50, chars)+"'\n")
