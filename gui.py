import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from datetime import date
import re #регулярные выражения

from database import init_db, seed_keys_if_empty, get_all_keys, get_key_by_id, issue_key
from main import send_email  # функция отправки email

# ======================
# Инициализация БД
# ======================
init_db()
seed_keys_if_empty()

# ======================
# Валидация вводимых данных
# ======================
def validate_inn(inn):
    return inn.isdigit() and len(inn) in (10, 12)

def validate_fio(fio):
    return bool(re.match(r"^[A-Za-zА-Яа-яЁё\s\-]+$", fio))

def validate_email(email):
    return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email))

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
    "DST", "Пароль", "Действие"
]

table = tk.Frame(root)
table.pack(fill="both", expand=True)

def refresh_table():
    for w in table.winfo_children():
        w.destroy()

    # Заголовки
    for col, h in enumerate(headers):
        tk.Label(table, text=h, bg="#eee", width=18).grid(row=0, column=col)

    keys = get_all_keys()
    for i, key in enumerate(keys):
        key_id, node_name, org, inn, fio, email, issue_date, dst, password, is_issued = key
        row = i * 2 + 1
        values = [node_name, org or "-", inn or "-", fio or "-", email or "-", issue_date or "-", dst or "-", password or "-"]

        # Labels
        for col, val in enumerate(values):
            tk.Label(table, text=val, width=18).grid(row=row, column=col)

        # Кнопка действия
        btn_text = "Выдать ключ" if not is_issued else "Редактировать ключ"
        tk.Button(
            table,
            text=btn_text,
            bg="#7E3FF2",
            fg="white",
            command=lambda k=key_id: open_issue_window(k)
        ).grid(row=row, column=len(headers) - 1)

        # Разделитель
        ttk.Separator(table, orient="horizontal").grid(
            row=row + 1, column=0, columnspan=len(headers), sticky="ew", pady=2
        )

#окно для выпуска ключа
def open_issue_window(key_id):
    key = get_key_by_id(key_id)
    if not key:
        messagebox.showerror("Ошибка", "Ключ не найден")
        return
#колонки из таблицы keys переводим в переменные
    key_id, node_name, org, inn, fio, email, issue_date, dst, password, is_issued = key

    win = tk.Toplevel(root)
    win.title("Выдача/Редактирование ключа")
    win.geometry("420x560")

    fields = {}
#добавление полей
    def add(label, value="", readonly=False):
        tk.Label(win, text=label).pack(anchor="w", padx=10)
        e = tk.Entry(win)
        e.pack(fill="x", padx=10, pady=4)
        e.insert(0, value or "")
        if readonly:
            e.config(state="readonly")
        fields[label] = e

    add("Название узла", node_name, True)
    add("Организация", org)
    add("ИНН", inn)
    add("ФИО", fio)
    add("Email", email)
    tk.Label(win, text="Дата выдачи").pack(anchor="w", padx=10)
    date_picker = DateEntry(win, maxdate=date.today(), date_pattern="yyyy-mm-dd")
    date_picker.pack(fill="x", padx=10, pady=4)
    if issue_date:
        date_picker.set_date(issue_date)
    add("DST", dst, True)
    add("Пароль", password, True)
#отправка пароля на почту
    def send_pass():
        email_val = fields["Email"].get()
        org_val = fields["Организация"].get()
        if not validate_email(email_val):
            messagebox.showerror("Ошибка", "Некорректный email")
            return
        try:
            send_email(email_val, org_val, password)
            messagebox.showinfo("Успех", "Пароль отправлен")
        except Exception as e:
            messagebox.showerror("Ошибка SMTP", str(e))
#ГУИ для добавления информации о ключах
    def issue_key_gui():
        inn_val = fields["ИНН"].get()
        fio_val = fields["ФИО"].get()
        email_val = fields["Email"].get()
        if not validate_inn(inn_val):
            messagebox.showerror("Ошибка", "ИНН некорректен")
            return
        if not validate_fio(fio_val):
            messagebox.showerror("Ошибка", "ФИО некорректно")
            return
        if not validate_email(email_val):
            messagebox.showerror("Ошибка", "Email некорректен")
            return
        # Обновляем в БД
        issue_key(
            key_id,
            fields["Организация"].get(),
            inn_val,
            fio_val,
            email_val,
            date_picker.get_date().isoformat()
        )
        refresh_table()
        win.destroy()

    btns = tk.Frame(win)
    btns.pack(pady=20)
    tk.Button(btns, text="Отправить пароль", bg="#7E3FF2", fg="white", command=send_pass).grid(row=0, column=0, padx=5)
    tk.Button(btns, text="Выдать/Сохранить ключ", bg="#7E3FF2", fg="white", command=issue_key_gui).grid(row=0, column=1, padx=5)
    tk.Button(btns, text="Отмена", command=win.destroy).grid(row=0, column=2, padx=5)

# ======================
# Запуск
# ======================
tk.Label(root, text="Список ключей", font=("Arial", 14)).pack(pady=10)
refresh_table()
root.mainloop()
