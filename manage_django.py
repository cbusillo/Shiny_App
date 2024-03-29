"""formerly manage.py from django project"""

import sys
import os


def main():
    """Run administrative tasks."""
    os.environ.setdefault(key="DJANGO_SETTINGS_MODULE", value="shiny_app.django_server.settings")
    try:
        from django.core.management import execute_from_command_line  # pylint: disable=import-outside-toplevel
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    if len(sys.argv) == 1:
        execute_from_command_line(
            [
                sys.argv[0],
                "runserver",
                "0.0.0.0:8000",
            ]
        )

    else:
        execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
