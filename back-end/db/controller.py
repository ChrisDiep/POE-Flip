from mongoengine import *
from dateutil.parser import parse
import models

import json


class Mongo:
    """ Database methods for updating/inserting """

    def __init__(self):
        self.db_name = "POE-Flip"
        connect(self.db_name)

    def __enter__(self):
        connect(self.db_name)
        return self

    def __exit__(self, *err):
        disconnect(self.db_name)

    def insert_currency(self, data):
        """ Inserts currency entry into database """
        models.Currency(
            currency_name=data["result"][0]["listing"]["price"]["exchange"]["currency"],
            icon=data["result"][0]["item"]["icon"],
            prices={},
        ).save()

    def insert_listings(self, curr, data):
        """ Inserts listings for a currency entry in the database """
        data = data["result"]
        listings = []
        for listing in data:
            listing = listing["listing"]
            listings.append(
                models.Listing(
                    name=listing["account"]["name"],
                    last_char=listing["account"]["lastCharacterName"],
                    posted=parse(listing["indexed"]),
                    want_curr=listing["price"]["exchange"]["currency"],
                    want_rate=listing["price"]["exchange"]["amount"],
                    has_curr=listing["price"]["item"]["currency"],
                    has_rate=listing["price"]["item"]["amount"],
                    has_stock=listing["price"]["item"]["stock"],
                )
            )
        models.Currency.objects(currency_name=curr).update(
            **{
                f"set__prices__{data[0]['listing']['price']['item']['currency']}": listings
            }
        )

    def find(self, curr):
        """ Returns then entry for a single currency """
        return models.Currency.objects(currency_name=curr).to_json()


with Mongo() as mongo:
    f = open("dummy.json")
    data = json.load(f)
    mongo.insert_currency(data)
    mongo.insert_listings("exalted", data)
    f.close()
