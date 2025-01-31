#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    # Set the default settings module for the 'DJANGO_SETTINGS_MODULE' environment variable.
    # This tells Django which settings file to use for the project.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Sleepify.settings')
    try:
        # Import and execute the command-line utility for Django.
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # If Django is not installed or there's an issue with the import,
        # raise an appropriate error message.
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # Execute the command line instructions passed to this script (like running the server, migrations, etc.)
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    # Calls the main function to run the administrative tasks.
    main()
