import re
from models import Quote
import redis

# Підключення до Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

def search_by_tags(tags):
    
    # Перевіряємо, чи результат не зберігався у кеші Redis
    tags_str = ','.join(tags)
    cached_result = redis_client.get(f'tags:{tags_str}')
    if cached_result:
        return cached_result.decode('utf-8')

    # Видаляємо можливі пробіли з тегів і виконуємо пошук у базі даних MongoDB
    cleaned_tags = [tag.strip() for tag in tags]
    quotes = Quote.objects(tags__in=cleaned_tags)
    result = '\n'.join([quote.quote for quote in quotes])

    # Зберігаємо результат у кеші Redis на 5 хвилин
    redis_client.setex(f'tags:{tags_str}', 300, result)
    return result

def search_quotes():
    # Функція для пошуку цитат за ім'ям автора, тегом або набором тегів
    while True:
        command = input("Введіть команду: ")

        if command.startswith('name:'):
            name = command.replace('name:', '').strip()
            result = search_by_author_name(name)
            print(result)
        elif command.startswith('tag:'):
            tag = command.replace('tag:', '').strip()
            result = search_by_tags([tag])
            print(result)
        elif command.startswith('tags:'):
            tags = command.replace('tags:', '').strip().split(',')
            result = search_by_tags(tags)
            print(result)
        elif command == 'exit':
            break
        else:
            print("Невірна команда. Спробуйте ще раз.")

def search_by_author_name(name):
    
    # Перевіряємо, чи результат не зберігався у кеші Redis
    cached_result = redis_client.get(f'author:{name}')
    if cached_result:
        return cached_result.decode('utf-8')
    print(f"Ім'я для пошуку: {name}")
    
    quotes = Quote.objects()
    
    # Фільтруємо цитати за ім'ям автора, використовуючи регулярний вираз у Python
    filtered_quotes = [quote for quote in quotes if re.search(f'.*{re.escape(name)}.*', quote.author.fullname, re.IGNORECASE)]


    
    
    result = '\n'.join([quote.quote for quote in filtered_quotes])
    print(f"Кількість знайдених цитат: {len(filtered_quotes)}")

    # Зберігаємо результат у кеші Redis на 5 хвилин
    redis_client.setex(f'author:{name}', 300, result)
    return result






