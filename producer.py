import pika
import json
from mongo_setup import setup_mongo_connection
import faker
import configparser
from mongoengine import Document, StringField, BooleanField

# Читання конфігураційних даних
config = configparser.ConfigParser()
config.read('config.ini')

# Підключення до MongoDB
setup_mongo_connection()

# Модель контакту
class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    sent = BooleanField(default=False)

def generate_and_send_contacts():
    # Підключення до RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # Створення черги для повідомлень
    channel.queue_declare(queue='email_queue')

    # Генерація фейкових контактів та надсилання їх у чергу
    fake = faker.Faker()
    for _ in range(10):  # Відправити 10 фейкових контактів
        contact_data = {
            "fullname": fake.name(),
            "email": fake.email()
        }
        contact = Contact(**contact_data)
        contact.save()

        # Надіслати ObjectID створеного контакту у чергу RabbitMQ
        message = {
            "contact_id": str(contact.id)
        }
        channel.basic_publish(exchange='',
                              routing_key='email_queue',
                              body=json.dumps(message))
        print(f" [x] Sent {message}")

    # Закриття з'єднання з RabbitMQ
    connection.close()

if __name__ == "__main__":
    generate_and_send_contacts()
