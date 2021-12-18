import tkinter as tk
from tkinter import ttk, messagebox
from functools import partial


g_captcha = '!EXIT'


def fetch_code(root: ttk.Entry, widget: ttk.Entry, *_):
    code = widget.get().strip()
    if len(code) != 6 and not code.isdigit():
        messagebox.showwarning("", "Введённый код невалиден")
    else:
        global g_captcha
        g_captcha = code
        root.destroy()


def solve(data: bytes):
    global g_captcha
    g_captcha = '!EXIT'

    root = tk.Tk()
    root.title("Captcha")
    img = tk.PhotoImage(data=data)
    canvas = ttk.Label(root, image=img, font=('Arial', 12))
    captcha_lb = ttk.Label(root, text='Code:', font=('Arial', 12))
    captcha_en = ttk.Entry(root, font=('Arial', 12))
    canvas.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
    captcha_lb.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
    captcha_en.grid(row=1, column=1, padx=5, pady=5, sticky=tk.NSEW)
    captcha_en.bind('<Return>', partial(fetch_code, root, captcha_en))
    captcha_en.focus_set()
    root.mainloop()

    return g_captcha
