import os
import tkinter as tk
from subprocess import call


def clear_window():
    _ = call("cls" if os.name.lower().startswith('win') else "clear")
