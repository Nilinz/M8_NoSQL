import redis
from mongoengine import connect
from models import Author, Quote
import configparser
from mongo_setup import setup_mongo_connection

# Читання конфігураційних даних

config = configparser.ConfigParser()
config.read('config.ini')

# Підключення до MongoDB
setup_mongo_connection()

# Підключення до Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
def search_quotes():
    
    while True:
        try:
            command = input("Введіть команду (наприклад, name: Steve Martin, tag: life, tags: life,live, exit для виходу): ")
            cached_result = redis_client.get(command)  # Перевірка результату в Redis кеші
            
            if cached_result:
                print("Знайдено в кеші:")
                print(cached_result)
                continue

            if command.startswith('name:') or command.startswith('tag:') or command.startswith('tags:'):
                if command.startswith('name:'):
                    search_type, search_value = command.split(': ')
                    search_type = 'name'
                elif command.startswith('tag:'):
                    search_type, search_value = command.split(': ')
                    search_type = 'tags'
                else:
                    search_type, search_value = command.split(': ')
                    search_type = 'tags'
                    search_value = search_value.replace(',', ' ')
                    
                if search_type == 'name':
                    author_name = search_value
                    author = Author.objects(name__icontains=author_name).first()
                    if author:
                        quotes = Quote.objects(author=author)
                        results = [quote.text for quote in quotes]
                    else:
                        results = ["Автор не знайдений."]
                elif search_type == 'tags':
                    tags = search_value.split()
                    quotes = Quote.objects(tags__in=tags)
                    results = [quote.text for quote in quotes]
                else:
                    results = ["Невірна команда. Спробуйте ще раз."]

                # Збереження результатів у Redis кеші
                redis_client.set(command, "\n".join(results))
                print("Результат збережено у Redis кеші:")
                print("\n".join(results))

            elif command == 'exit':
                break

            else:
                print("Невірна команда. Спробуйте ще раз.")

        except Exception as e:
            print(f"Помилка: {e}")

if __name__ == "__main__":
    search_quotes()
