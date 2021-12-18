import os
import random
import string
from subprocess import call


def clear_window():
    _ = call("cls" if os.name.lower().startswith('win') else "clear")


def gen_password(length: int = 12):
    return ''.join(random.choices(string.digits + string.ascii_letters, k=length))
