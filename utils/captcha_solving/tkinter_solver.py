import tkinter as tk
import time
from tkinter import ttk, messagebox


class TkinterSolver:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Captcha")
        self.root.withdraw()

        self.canvas = ttk.Label(self.root, font=('Arial', 12))
        self.captcha_lb = ttk.Label(self.root, text='Code:', font=('Arial', 12))
        self.captcha_en = ttk.Entry(self.root, font=('Arial', 12))

        self.canvas.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        self.captcha_lb.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.captcha_en.grid(row=1, column=1, padx=5, pady=5, sticky=tk.NSEW)

        self.result_ = None

    def solve(self, data):
        img = tk.PhotoImage(data=data)
        self.canvas.configure(image=img)

        self.captcha_en.bind('<Return>', self.fetch_code)
        self.root.deiconify()

        self.captcha_en.focus_set()
        while self.result_ is None:
            self.root.update()
            time.sleep(0.05)
        self.root.withdraw()

        real_result = self.result_
        self.result_ = None
        return real_result

    def fetch_code(self, *_):
        code = self.captcha_en.get().strip()
        if len(code) != 6 or not code.isdigit():
            messagebox.showwarning("", "Введённый код невалиден")
        else:
            self.result_ = code
        self.captcha_en.delete(0, tk.END)

    def __del__(self):
        try:
            self.root.destroy()
        except Exception:
            pass
