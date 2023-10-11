from mongoengine import Document, StringField, ReferenceField, BooleanField

class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField(required=True)
    born_location = StringField(required=True)
    description = StringField(required=True)

class Quote(Document):
    tags = StringField(required=True)
    author = ReferenceField(Author)
    quote = StringField(required=True)

class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    message_sent = BooleanField(default=False)
