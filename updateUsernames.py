import os, django, sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pizza.settings")
django.setup()
from orders.models import Size, Category, Item, Addition, OrderItem
from django.conf import settings
from django.contrib.auth.models import User

def main():

    print(auth.User)
    #users = settings.AUTH_USER_MODEL.all()

    #for i in users:
    #    print(i)

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pizza.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    main()