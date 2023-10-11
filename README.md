# M8_NoSQL

## Для проекту потрібно встановити програми:

- MongoDB: Для роботи з базою даних MongoDB. Можна завантажити з офіційного сайту MongoDB: https://www.mongodb.com/try/download/community
  
- Redis: Для використання Redis як системи кешування. Можна завантажити з офіційного сайту: https://redis.io/download/

Встановіть модуль ``Redis`` в корені проекту:
  ```
  pip install redis-lru
  ```
  
- RabbitMQ: Для використання RabbitMQ як системи черги повідомлень. Можна завантажити з офіційного сайту: https://www.rabbitmq.com/download.html

Встановіть локально сервіс RabbitMQ за допомогою Docker-образу.
```
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.11-management
```

## Запуск проекту

Створіть конфігураційний файл ``config.ini`` з налаштуваннями для підключення до вашої MongoDB бази даних. Ваш файл ``config.ini`` може виглядати так:

```
[mongodb]
uri = mongodb+srv://username:password@cluster.mongodb.net/mydatabase

```

Запустіть ``main.py`` 

```
py main.py
```

Вибирайте подальші опції, які ви хочете виконати.

### За допомогою пошуку по цитатами є команди:
- name: [ім'я] - Шукати цитати за ім'ям автора. Наприклад, name: Albert Einstein.
- tag: [тег] - Шукати цитати за конкретним тегом. Наприклад, tag: life.
- tags: [тег1, тег2, тег3] - Шукати цитати за набором тегів. Наприклад, tags: life, inspiration.
- exit - Вийти з програми.


