from producer import generate_and_send_contacts
from consumer import process_messages_and_send_email
from search_quotes import search_quotes
from load_data import load_data
import sys

def print_menu():
    print("Меню:")
    print("1. Завантажити дані з JSON файлів до бази даних")
    print("2. Згенерувати та відправити фейкові контакти у чергу RabbitMQ")
    print("3. Обробити повідомлення з черги RabbitMQ та надіслати email")
    print("4. Пошук цитат")
    print("5. Вийти")


def main():
    while True:
        print_menu()
        choice = input("Оберіть опцію: ")
        if choice == '1':
            load_data()
        elif choice == '2':
            generate_and_send_contacts()
        elif choice == '3':
            process_messages_and_send_email()
        elif choice == '4':
            search_quotes()
        elif choice == '5':
            print("До побачення!")
            break
        else:
            print("Невірний вибір. Будь ласка, спробуйте ще раз.")

if __name__ == "__main__":
    main()
    input("Натисніть Enter, щоб вийти...")
