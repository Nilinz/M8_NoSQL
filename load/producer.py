import json
import random
import string
import pika
from config import rabbitmq_config

# Налаштування підключення до RabbitMQ
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=rabbitmq_config['host'],
                              credentials=pika.PlainCredentials(rabbitmq_config['username'],
                                                              rabbitmq_config['password']))
)
channel = connection.channel()

# Створення черги для відправки повідомлень
channel.queue_declare(queue='email_queue')

# Генерація фейкових контактів та відправлення їх в чергу RabbitMQ
for _ in range(10):  # Генеруємо 10 фейкових контактів
    email = ''.join(random.choices(string.ascii_lowercase, k=8)) + '@example.com'
    message_body = f"Новий контакт: {email}"
    channel.basic_publish(exchange='', routing_key='email_queue', body=message_body)

    print(f"Відправлено: {message_body}")

# Закриття з'єднання з RabbitMQ
connection.close()
