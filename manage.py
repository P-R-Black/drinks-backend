#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import environ
import os
import sys
from drink_book.settings import base

env = environ.Env()
environ.Env.read_env()
print('test', base.DEBUG)


def main():
    """Run administrative tasks."""
    if base.DEBUG == 'True':
        print('test after if true', base.DEBUG)
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drink_book.settings.development')
    else:
        print('test after if false', base.DEBUG)
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drink_book.settings.production')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
