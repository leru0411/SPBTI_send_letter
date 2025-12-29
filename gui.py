import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from datetime import date
import random
import string
import re

from main import send_email   


# ======================
# ВАЛИДАЦИЯ
# ======================

def validate_inn(inn):
    return inn.isdigit() and len(inn) in (10, 12)


def validate_fio(fio):
    return bool(re.match(r"^[A-Za-zА-Яа-яЁё\s\-]+$", fio))


def validate_email(email):
    return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email))


# ======================
# COPY
# ======================

def copy_to_clipboard(text):
    if not text:
        return
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()


# ======================
# ПСЕВДОБД
# ======================

def gen_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))


def gen_dst():
    return ''.join(random.choices(string.ascii_letters, k=8)) + ".dst"


keys_storage = []
for i in range(10):
    keys_storage.append({
        "node": f"Ключ {i + 1}",
        "org": "",
        "inn": "",
        "fio": "",
        "email": "",
        "date": "",
        "dst": gen_dst(),
        "password": gen_password(),
        "issued": False
    })


# ======================
# GUI
# ======================

root = tk.Tk()
root.title("Выдача ключей ViPNet")
root.geometry("1300x450")
root.configure(bg="white")

headers = [
    "Название узла", "Организация", "ИНН",
    "ФИО", "Email", "Дата",
    "DST", "Пароль", ""
]


def refresh_table():
    for w in table.winfo_children():
        w.destroy()

    for col, h in enumerate(headers):
        tk.Label(table, text=h, bg="#eee", width=18).grid(row=0, column=col)

    for i, key in enumerate(keys_storage):
        row = i * 2 + 1
        values = [
            key["node"], key["org"], key["inn"],
            key["fio"], key["email"],
            key["date"], key["dst"], key["password"]
        ]

        for col, val in enumerate(values):
            lbl = tk.Label(table, text=val or "-", width=18, cursor="hand2")
            lbl.grid(row=row, column=col)
            lbl.bind("<Button-1>", lambda e, v=val: copy_to_clipboard(v))

        tk.Button(
            table,
            text="Выдать ключ",
            bg="#7E3FF2",
            fg="white",
            command=lambda idx=i: open_issue_window(idx)
        ).grid(row=row, column=len(headers) - 1)

        ttk.Separator(table, orient="horizontal").grid(
            row=row + 1, column=0, columnspan=len(headers), sticky="ew", pady=2
        )


def open_issue_window(index):
    key = keys_storage[index]

    win = tk.Toplevel(root)
    win.title("Выдача ключа")
    win.geometry("420x560")

    fields = {}

    def add(label, value="", readonly=False):
        tk.Label(win, text=label).pack(anchor="w", padx=10)
        e = tk.Entry(win)
        e.pack(fill="x", padx=10, pady=4)
        e.insert(0, value)
        if readonly:
            e.config(state="readonly")
        fields[label] = e

    add("Название узла", key["node"], True)
    add("Организация")
    add("ИНН")
    add("ФИО")
    add("Email")

    tk.Label(win, text="Дата выдачи").pack(anchor="w", padx=10)
    date_picker = DateEntry(win, maxdate=date.today(), date_pattern="yyyy-mm-dd")
    date_picker.pack(fill="x", padx=10, pady=4)

    add("DST", key["dst"], True)
    add("Пароль", key["password"], True)

    def send_pass():
        email = fields["Email"].get()
        organization = fields["Организация"].get()


        if not validate_email(email):
            messagebox.showerror("Ошибка", "Некорректный email")
            return

        try:
            send_email(email, organization, key["password"])
            messagebox.showinfo("Успех", "Пароль отправлен")
        except Exception as e:
            messagebox.showerror("Ошибка SMTP", str(e))

    def issue_key():
        inn = fields["ИНН"].get()
        fio = fields["ФИО"].get()
        email = fields["Email"].get()

        if not validate_inn(inn):
            messagebox.showerror("Ошибка", "ИНН некорректен")
            return
        if not validate_fio(fio):
            messagebox.showerror("Ошибка", "ФИО некорректно")
            return
        if not validate_email(email):
            messagebox.showerror("Ошибка", "Email некорректен")
            return

        key.update({
            "org": fields["Организация"].get(),
            "inn": inn,
            "fio": fio,
            "email": email,
            "date": date_picker.get_date().isoformat(),
            "issued": True
        })

        refresh_table()
        win.destroy()

    btns = tk.Frame(win)
    btns.pack(pady=20)

    tk.Button(btns, text="Отправить пароль", command=send_pass).grid(row=0, column=0, padx=5)
    tk.Button(btns, text="Выдать ключ", command=issue_key).grid(row=0, column=1, padx=5)
    tk.Button(btns, text="Отмена", command=win.destroy).grid(row=0, column=2, padx=5)


tk.Label(root, text="Список ключей", font=("Arial", 14)).pack(pady=10)
table = tk.Frame(root)
table.pack(fill="both", expand=True)

refresh_table()
root.mainloop()

