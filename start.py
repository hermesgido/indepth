import os
import sys
import subprocess
from django.contrib.auth import get_user_model


def create_superuser():
    try:
        User = get_user_model()
        if not User.objects.filter(username='admin@gmail.com').exists():
            User.objects.create_superuser(
                username='admin@gmail.com', password='12456')
            print("Superuser 'admin' created successfully.")
        else:
            print("Superuser 'admin' already exists.")
    except Exception as e:
        print(f"Error creating superuser: {e}")
        sys.exit(1)


def run_commands():
    commands = [
        'python manage.py makemigrations',
        'python manage.py migrate',
        'python manage.py generate_slots',
        'python manage.py generate_facilities',
        'python manage.py runserver'
    ]

    for command in commands:
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error executing {command}: {e}")
            sys.exit(1)

    create_superuser()


if __name__ == '__main__':
    run_commands()
