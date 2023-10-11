from load_data import load_data
from producer import send_fake_contacts
from consumer import consume_messages
from search_quotes import search_quotes
import pymongo
from config import get_mongo_uri
from mongoengine import connect 



def print_menu():
    print("Меню:")
    print("1. Завантажити дані з JSON файлів до бази даних")
    print("2. Згенерувати та відправити фейкові контакти у чергу RabbitMQ")
    print("3. Обробити повідомлення з черги RabbitMQ та надіслати email")
    print("4. Пошук цитат")
    print("5. Вийти")

def main():
    
    mongo_uri = get_mongo_uri()

    
    connect(host=mongo_uri)  
    while True:
        print_menu()
        choice = input("Виберіть опцію: ")

        if choice == "1":
            load_data()
        elif choice == "2":
            send_fake_contacts()
        elif choice == "3":
            consume_messages()
        elif choice == "4":
            search_quotes()
        elif choice == "5":
            print("Дякую за використання програми. До побачення!")
            break
        else:
            print("Невірний вибір опції. Будь ласка, спробуйте ще раз.")

if __name__ == "__main__":
    main()
