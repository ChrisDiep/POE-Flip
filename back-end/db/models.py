from mongoengine import *
from datetime import datetime

class Listing(EmbeddedDocument):
    name = StringField(required=True)
    last_char = StringField(required=True)
    posted = DateTimeField()
    want_curr = StringField(required=True)
    want_rate = IntField()
    has_curr = StringField(required=True)
    has_rate = IntField()
    has_stock = IntField()

class Currency(Document):
    currency_name = StringField(required=True)
    icon = StringField(required=True)
    last_updated = DateTimeField(default=datetime.utcnow())
    prices = MapField(ListField(EmbeddedDocumentField(Listing)))

