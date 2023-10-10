from mongoengine import Document, StringField, ReferenceField
import redis

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField(required=True)
    born_location = StringField(required=True)
    description = StringField(required=True)

class Quote(Document):
    tags = StringField(required=True)
    author = ReferenceField(Author)
    quote = StringField(required=True)

    @classmethod
    def search_quotes(cls, query_type, query_value):
        cache_key = f"{query_type}:{query_value}"
        cached_result = redis_client.get(cache_key)
        if cached_result:
            return cached_result.decode('utf-8')
        else:
            if query_type == "name":
                author = Author.objects(fullname__icontains=query_value).first()
                if author:
                    quotes = cls.objects(author=author).to_json()
                    redis_client.setex(cache_key, 60, quotes)
                    return quotes
            elif query_type == "tag":
                quotes = cls.objects(tags__icontains=query_value).to_json()
                redis_client.setex(cache_key, 60, quotes)
                return quotes
            elif query_type == "tags":
                tags = query_value.split(',')
                quotes = cls.objects(tags__in=tags).to_json()
                redis_client.setex(cache_key, 60, quotes)
                return quotes
            return "No results found."

