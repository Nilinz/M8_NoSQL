import pika
import json
from models import Contact
from faker import Faker

def send_fake_contacts():
    fake = Faker()

    # Підключення до RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Створення черги
    channel.queue_declare(queue='contacts')

    # Генерація фейкових контактів та відправлення їх у чергу RabbitMQ
    for _ in range(10):
        contact = Contact(
            fullname=fake.name(),
            email=fake.email()
        )
        contact.save()

        # Відправлення ObjectID контакту у чергу RabbitMQ
        message = {
            'contact_id': str(contact.id)
        }
        channel.basic_publish(exchange='', routing_key='contacts', body=json.dumps(message))
        print(f" [x] Sent {message}")

    
    connection.close()


if __name__ == "__main__":
    send_fake_contacts()