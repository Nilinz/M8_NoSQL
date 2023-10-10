from mongoengine import Document, StringField, ReferenceField, ListField

class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField(required=True)
    born_location = StringField(required=True)
    description = StringField(required=True)


class Quote(Document):
    text = StringField(required=True)
    tags = ListField(StringField())
    author = ReferenceField(Author)
