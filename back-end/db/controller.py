from mongoengine import *
from dateutil.parser import parse
from datetime import datetime, timezone
from db import models

import json


class Mongo:
    """ Database methods for updating/inserting """

    def __init__(self, reverse_currency_ref=None):
        self.db_name = "POE-Flip"
        self.ref = reverse_currency_ref

    def __enter__(self):
        connect(self.db_name)
        return self

    def __exit__(self, *err):
        disconnect(self.db_name)

    def _get_curr_name(self, short_name):
        if self.ref is not None:
            return self.ref[short_name]["text"]
        return short_name

    def insert_currency(self, data):
        """ Inserts currency entry into database """
        models.Currency.objects(
            currency_name=data["listing"]["price"]["exchange"]["currency"]
        ).update(
            **{
                "currency_name": self._get_curr_name(
                    data["listing"]["price"]["exchange"]["currency"]
                ),
                "icon": data["item"]["icon"],
                "prices": {},
            },
            upsert=True,
        )

    def insert_listings(self, curr, data):
        """ Inserts listings for a currency entry in the database """
        data = data["result"]
        listings = []
        for listing in data:
            listing = listing["listing"]
            online_info = listing["account"]["online"]
            status = online_info["status"] if "status" in online_info else "online"
            listings.append(
                models.Listing(
                    name=listing["account"]["name"],
                    last_char=listing["account"]["lastCharacterName"],
                    posted=parse(listing["indexed"]),
                    status=status,
                    league=online_info["league"],
                    whisper=listing["whisper"],
                    language=listing["account"]["language"],
                    want_curr=self._get_curr_name(
                        listing["price"]["exchange"]["currency"]
                    ),
                    want_rate=listing["price"]["exchange"]["amount"],
                    has_curr=self._get_curr_name(listing["price"]["item"]["currency"]),
                    has_rate=listing["price"]["item"]["amount"],
                    has_stock=listing["price"]["item"]["stock"],
                )
            )
        models.Currency.objects(currency_name=self._get_curr_name(curr)).update(
            **{
                f"set__prices__{self._get_curr_name(data[0]['listing']['price']['item']['currency'])}": listings
            }
        )

    def insert_entries(self, data):
        for results in data:
            if results[0] is not None:
                self.insert_currency(results[0]["result"][0])
                for result in results:
                    if result is not None:
                        self.insert_listings(
                            result["result"][0]["listing"]["price"]["exchange"][
                                "currency"
                            ],
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
            currencies[currency["currencyTypeName"]] = models.ChaosEquivListing(
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

    def insert_static_info(self, data):
        data_list = data["result"]
        for group in data_list:
            entries = []
            for entry in group["entries"]:
                entries.append(models.EntryInfo(
                    official_id=entry["id"],
                    text=entry["text"],
                    image=entry["image"] if "image" in entry else None
                ))
            models.StaticInfo.objects(
                field_id=group["id"]
            ).update(
                **{
                    "field_id": group["id"],
                    "label": group["label"],
                    "entries": entries
                },
                upsert=True,
            )

    def get_static_info(self):
        return models.StaticInfo.objects.to_json()
# with Mongo() as mongo:
#     f = open("dummy2.json")
#     data = json.load(f)
#     # mongo.insert_currency(data)
#     # mongo.insert_listings("exalted", data)
#     mongo.insert_entries(data)
#     f.close()
#     # print(mongo.get_stale_entries())
