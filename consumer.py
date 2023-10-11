import pika
import json
from models import Contact

def consume_messages():
    # Підключення до RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Створення черги
    channel.queue_declare(queue='contacts')

    # Функція для обробки повідомлень з черги RabbitMQ
    def callback(ch, method, properties, body):
        contact_id = json.loads(body)['contact_id']
        contact = Contact.objects(id=contact_id).first()

        if contact:
            # Оновлення значення поля 'message_sent' контакту на True
            contact.update(set__message_sent=True)
            print(f" [x] Updated message sent status for contact {contact.fullname}")

    # Вказуємо, що функція callback обробляє повідомлення з черги
    channel.basic_consume(queue='contacts', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    # Запускаємо обробку повідомлень з черги RabbitMQ
    channel.start_consuming()

# Ця умовна конструкція дозволяє запускати цей файл як скрипт або імпортувати його функції в інших файлах
if __name__ == "__main__":
    consume_messages()