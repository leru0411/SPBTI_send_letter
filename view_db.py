import sqlite3
from tabulate import tabulate  # для красивой таблицы

# Подключаемся к БД
conn = sqlite3.connect("vipnet.db")
cursor = conn.cursor()

# Получаем список таблиц
sql_request = "SELECT * FROM keys WHERE is_issued = 1;"
# cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
cursor.execute(sql_request)
rows = cursor.fetchall()
columns = [desc[0] for desc in cursor.description]  # имена столбцов
print(tabulate(rows, headers=columns, tablefmt="grid"))



conn.close()
