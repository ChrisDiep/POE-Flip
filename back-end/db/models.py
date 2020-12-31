from mongoengine import *
from datetime import datetime, timezone


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
    last_updated = DateTimeField(default=datetime.now(timezone.utc))
    prices = MapField(ListField(EmbeddedDocumentField(Listing)))


class ChaosEquivListing(EmbeddedDocument):
    buy_price = DecimalField(precision=1, null=True)
    buy_listings = IntField(null=True)
    sell_price = DecimalField(precision=1, null=True)
    sell_listings = IntField(null=True)


class ChaosEquivalent(Document):
    last_updated = DateTimeField(default=datetime.now(timezone.utc))
    info = MapField(EmbeddedDocumentField(ChaosEquivListing))
