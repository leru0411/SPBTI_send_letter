import smtplib
from email.message import EmailMessage

SMTP_SERVER = "smtp.yandex.ru"
SMTP_PORT = 465

EMAIL_FROM = "email"
EMAIL_PASSWORD = "pass"

def send_email(to_email, organization, password):
    msg = EmailMessage()
    msg["From"] = EMAIL_FROM
    msg["To"] = to_email
    msg["Subject"] = "Пароль от випнет"

    msg.set_content(f"""
Здравствуйте!

Для организации "{organization}" был выдан ключ ViPNet.

Пароль для ключа випнета: {password}

Пересылать пароль третьим лицам запрещено, в противном случае ключ будет заблокирован.
""")

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.send_message(msg)

    print("Письмо отправлено")

# # тест
# send_email(
#     to_email="leru0411@mail.ru",
#     organization="ООО Ромашка",
#     password="X7kP92Lm"
# )
    # try:
    #     with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
    #         server.login(EMAIL_FROM, EMAIL_PASSWORD)
    #         server.send_message(msg)
    #     messagebox.showinfo("Успех", "Письмо отправлено!")
    # except Exception as e:
    #     messagebox.showerror("Ошибка", f"Не удалось отправить письмо:\n{e}")
# ----------------- Логика выдачи ключа -----------------
def issue_key(data_dict):
    """
    Пока просто выводим в консоль.
    В будущем здесь будет сохранение в БД.
    """
    if all(data_dict.values()):
        print("=== Данные ключа ===")
        for k, v in data_dict.items():
            print(f"{k}: {v}")
        print("===================")
        return True
    else:
        return False