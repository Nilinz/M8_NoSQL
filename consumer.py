import pika
from config import rabbitmq_config

# Налаштування підключення до RabbitMQ
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=rabbitmq_config['host'],
                              credentials=pika.PlainCredentials(rabbitmq_config['username'],
                                                              rabbitmq_config['password']))
)
channel = connection.channel()

# Створення черги для споживача
channel.queue_declare(queue='email_queue')


def send_email(message_body):
    # Логіка надсилання email
    # ...


def callback(ch, method, properties, body):
    print(f"Отримано повідомлення: {body}")
    send_email(body)  # Виклик функції для надсилання email


# Вказуємо, яку функцію використовувати як обробник повідомлень з черги
channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)

print('Споживач чекає на повідомлення. Для виходу натисніть CTRL+C')
channel.start_consuming()
