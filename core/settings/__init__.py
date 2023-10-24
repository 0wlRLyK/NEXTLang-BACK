# settings/__init__.py
import sys

# Define the current command passed to manage.py.
current_command = None
if len(sys.argv) > 1:
    current_command = sys.argv[1]

# Set the settings based on the command.
if current_command == "runserver":
    from .dev import *  # type: ignore # noqa
elif current_command == "test":
    from .test import *  # type: ignore # noqa
else:
    from .production import *  # type: ignore # noqa
