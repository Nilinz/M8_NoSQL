import json
from database.models import Author, Quote

# Завантаження даних з JSON файлів та зберігання їх в базі даних MongoDB
with open('authors.json', 'r', encoding='utf-8') as authors_file:
    authors_data = json.load(authors_file)

    for author_info in authors_data:
        author = Author(**author_info)
        author.save()

with open('quotes.json', 'r', encoding='utf-8') as quotes_file:
    quotes_data = json.load(quotes_file)

    for quote_info in quotes_data:
        author_name = quote_info['author']
        author = Author.objects(fullname=author_name).first()
        quote_info['author'] = author  # Встановлюємо посилання на об'єкт автора

        quote = Quote(**quote_info)
        quote.save()

print('Дані успішно завантажено до бази даних MongoDB.')
