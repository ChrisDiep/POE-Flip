from mongoengine import *
from dateutil.parser import parse
from datetime import datetime, timezone
from db import models

import json


class Mongo:
    """ Database methods for updating/inserting """

    def __init__(self):
        self.db_name = "POE-Flip"

    def __enter__(self):
        connect(self.db_name)
        return self

    def __exit__(self, *err):
        disconnect(self.db_name)

    def insert_currency(self, data):
        """ Inserts currency entry into database """
        models.Currency(
            currency_name=data["listing"]["price"]["exchange"]["currency"],
            icon=data["item"]["icon"],
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

    def insert_entries(self, data):
        for results in data:
            self.insert_currency(results[0]["result"][0])
            for result in results:
                self.insert_listings(
                    result["result"][0]["listing"]["price"]["exchange"]["currency"],
                    result,
                )

    def get_total_entries(self):
        results = json.loads(models.Currency.objects().to_json())
        entries = []
        for result in results:
            entries.append(result["currency_name"])
        return entries

    def get_stale_entries(self):
        results = json.loads(models.Currency.objects().to_json())
        stale_entries = []
        for result in results:
            if self._is_stale(result):
                currency_name = result["currency_name"]
                stale_entries.append(currency_name)
        return stale_entries

    def _is_stale(self, result):
        """ Checks if data in the db is older than a minute """
        date = result["last_updated"]["$date"] / 1000
        now_minus_one_minute = datetime.now(timezone.utc).timestamp() - 60
        return date < now_minus_one_minute

    def find_currency(self, curr=""):
        """ Returns then entry for a given currency or all if none are given """
        if curr == "":
            return models.Currency.objects.to_json()
        else:
            return models.Currency.objects(currency_name=curr).to_json()

    def insert_chaos_equiv(self, data):
        currencies_data = data["lines"]
        currencies = {}
        for currency in currencies_data:
            currencies[currency["detailsId"]] = models.ChaosEquivListing(
                buy_price=round(currency["receive"]["value"], 1)
                if currency["receive"]
                else None,
                buy_listings=currency["receive"]["count"]
                if currency["receive"]
                else None,
                sell_price=round(1 / currency["pay"]["value"], 1)
                if currency["pay"]
                else None,
                sell_listings=currency["pay"]["count"] if currency["pay"] else None,
            )
        models.ChaosEquivalent(
            info=currencies,
        ).save()

    def find_chaos_equiv(self):
        return models.ChaosEquivalent.objects.to_json()


# with Mongo() as mongo:
#     f = open("dummy2.json")
#     data = json.load(f)
#     # mongo.insert_currency(data)
#     # mongo.insert_listings("exalted", data)
#     mongo.insert_entries(data)
#     f.close()
#     # print(mongo.get_stale_entries())
