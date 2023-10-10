import json
from mongoengine import connect
from models import Author, Quote
from mongo_setup import setup_mongo_connection

def load_data():
    setup_mongo_connection()

    # Завантаження даних з JSON файлів
    with open('authors.json', 'r', encoding='utf-8') as file:
        authors_data = json.load(file)

    with open('quotes.json', 'r', encoding='utf-8') as file:
        quotes_data = json.load(file)

    # Збереження даних в базі даних MongoDB
    for author_data in authors_data:
        fullname = author_data['fullname']
        born_date = author_data['born_date']
        born_location = author_data['born_location']
        description = author_data['description']
        
        author = Author(fullname=fullname, born_date=born_date, born_location=born_location, description=description)
        author.save()

    for quote_data in quotes_data:
        author_name = quote_data['author']
        text = quote_data['quote']
        tags = quote_data['tags']
        
        author = Author.objects(fullname=author_name).first()
        quote = Quote(text=text, tags=tags, author=author)
        quote.save()

if __name__ == "__main__":
    load_data()
    print("Data loaded successfully.")
