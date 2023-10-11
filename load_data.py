import json
import pymongo
from config import get_mongo_uri

def load_data():
    # Зчитування URI для MongoDB з конфігураційного файлу
    mongo_uri = get_mongo_uri()

    # Підключення до MongoDB
    client = pymongo.MongoClient(mongo_uri)
    db = client.get_database()

    # Зчитування даних з JSON файлів та збереження в базу даних
    with open('authors.json', 'r', encoding='utf-8') as authors_file:
        authors_data = json.load(authors_file)
        db.authors.insert_many(authors_data)

    with open('quotes.json', 'r', encoding='utf-8') as quotes_file:
        quotes_data = json.load(quotes_file)
        db.quotes.insert_many(quotes_data)

    print("Дані успішно завантажено до бази даних.")

if __name__ == "__main__":
    load_data()