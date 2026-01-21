import smtplib #библиотека для отправки сообщений по протоколу SMTP
from email.message import EmailMessage #конструктор письма

SMTP_SERVER = "smtp.yandex.ru"
SMTP_PORT = 465

EMAIL_FROM = ""
EMAIL_PASSWORD = ""

#метод отправки сообщения по email
def send_email(to_email, organization, password):
    msg = EmailMessage()
    msg["From"] = EMAIL_FROM
    msg["To"] = to_email
    msg["Subject"] = "Пароль от випнет"

#создание тела письма
    msg.set_content(f"""
Здравствуйте!

Для организации "{organization}" был выдан ключ ViPNet.

Пароль для ключа випнета: {password}

Пересылать пароль третьим лицам запрещено, в противном случае ключ будет заблокирован.
""")

#подключение к SMTP
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.send_message(msg)

    print("Письмо отправлено")
