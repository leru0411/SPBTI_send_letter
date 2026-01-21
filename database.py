import sqlite3
import random
import string

DB_NAME = "vipnet.db"


def get_connection(): #подключение к БД
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()
    cur = conn.cursor()
#создание таблицы keys
    cur.execute("""
        CREATE TABLE IF NOT EXISTS keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            node_name TEXT,
            organization TEXT,
            inn TEXT,
            fio TEXT,
            email TEXT,
            issue_date TEXT,
            dst_file TEXT,
            password TEXT,
            is_issued INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()

#генерация пароля для ключа
def generate_password(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

#генерация названия ключа
def generate_dst():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8)) + ".dst"

#генерация ключей
def seed_keys_if_empty():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM keys")
    count = cur.fetchone()[0]

    if count == 0:
        for i in range(1, 11):
            cur.execute("""
                INSERT INTO keys (node_name, dst_file, password)
                VALUES (?, ?, ?)
            """, (
                f"Ключ {i}",
                generate_dst(),
                generate_password()
            ))

    conn.commit()
    conn.close()

#метод вытаскивания ключей
def get_all_keys():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM keys")
    rows = cur.fetchall()

    conn.close()
    return rows


def get_key_by_id(key_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM keys WHERE id = ?", (key_id,))
    row = cur.fetchone()

    conn.close()
    return row

#метод выдачи ключа
def issue_key(key_id, organization, inn, fio, email, issue_date):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE keys
        SET organization = ?,
            inn = ?,
            fio = ?,
            email = ?,
            issue_date = ?,
            is_issued = 1
        WHERE id = ?
    """, (
        organization,
        inn,
        fio,
        email,
        issue_date,
        key_id
    ))

    conn.commit()
    conn.close()
