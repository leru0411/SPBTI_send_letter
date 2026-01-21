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

# tables = [t[0] for t in cursor.fetchall()]

# if not tables:
#     print("В базе данных нет таблиц")
# else:
#     for table in tables:
#         print(f"\n===== Таблица: {table} =====")
#         # Получаем названия столбцов
#         cursor.execute(f"PRAGMA table_info({table});")
#         columns = [info[1] for info in cursor.fetchall()]
#         # Получаем все данные
#         cursor.execute(f"SELECT * FROM {table};")
#         rows = cursor.fetchall()
#         # Выводим красиво через tabulate
#         if rows:
#             print(tabulate(rows, headers=columns, tablefmt="grid"))
#         else:
#             print("(Таблица пуста)")



conn.close()
