import pika
import json
from mongo_setup import setup_mongo_connection
import configparser
from mongoengine import Document, StringField, BooleanField


# Читання конфігураційних даних
config = configparser.ConfigParser()
config.read('config.ini')

# Підключення до MongoDB
setup_mongo_connection()

class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    sent = BooleanField(default=False)


def process_messages_and_send_email():
    # Підключення до RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # Створення черги для повідомлень
    channel.queue_declare(queue='email_queue')

    # Функція для імітації надсилання email
    def send_email(contact_data):
        print(f"Sent email to {contact_data['email']}")

    # Функція для обробки отриманих повідомлень
    def callback(ch, method, properties, body):
        message = json.loads(body)
        contact_id = message.get("contact_id")

        # Знаходження контакту за ID
        contact = Contact.objects(id=contact_id, sent=False).first()
        if contact:
            # Логіка для імітації надсилання email контакту
            send_email({"email": contact.email})
            # Позначення контакту як надісланого
            contact.sent = True
            contact.save()

        print(f"Processed message for contact ID: {contact_id}")

    # Підписка на чергу для отримання повідомлень
    channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

# Ця умова потрібна, щоб можна було імпортувати функцію process_messages_and_send_email
if __name__ == "__main__":
    process_messages_and_send_email()
