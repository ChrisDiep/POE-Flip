import json
import asyncio
from datetime import datetime, timezone
from server.models.api_calls import POEOfficial, POENinja
from db.controller import Mongo

currencies = [
    "Exalted Orb",
    "Chaos Orb",
    "Divine Orb",
    "Orb of Fusing",
    "Orb of Alteration",
]
currency_ref = None
reverse_currency_ref = None
poe_official_currencies = []
LEAGUE = "Heist"
DELAY = 1.4


def _get_chaos_equiv(db):
    chaos_equivalents = json.loads(db.find_chaos_equiv())
    chaos_equiv = chaos_equivalents[-1] if len(chaos_equivalents) != 0 else None
    updated_at = (
        (chaos_equiv["last_updated"]["$date"] / 1000)
        if chaos_equiv is not None
        else None
    )
    now_minus_one_day = datetime.now(timezone.utc).timestamp() - (60 * 60 * 24)
    if chaos_equiv is not None and updated_at > now_minus_one_day:
        return chaos_equiv
    else:
        poe_ninja = POENinja(LEAGUE)
        response = asyncio.run(poe_ninja.get_currencies())
        db.insert_chaos_equiv(response)
        return json.loads(db.find_chaos_equiv())[-1]


def _parse_currency_ref(api):
    global currency_ref
    global reverse_currency_ref
    global poe_official_currencies
    new_poe_official_currencies = []
    if currency_ref is None:
        currencies_info = asyncio.run(api.get_currency_ref())["result"][0]["entries"]
        currency_info = {}
        reverse_currency_info = {}
        for currency in currencies_info:
            currency_info[currency["text"]] = {
                "id": currency["id"],
                "image": currency["image"],
            }
            reverse_currency_info[currency["id"]] = {"text": currency["text"]}
        currency_ref = currency_info
        reverse_currency_ref = reverse_currency_info
        for currency in currencies:
            new_poe_official_currencies.append(currency_ref[currency]["id"])
        poe_official_currencies = new_poe_official_currencies


def get_time_estimate_seconds():
    time_estimate = DELAY * (len(currencies) - 1) * len(currencies)
    return time_estimate


def update_listings():
    poe_official = POEOfficial("placeholder", LEAGUE)
    _parse_currency_ref(poe_official)
    total_time = get_time_estimate_seconds()
    elapsed_time = 0
    with Mongo(reverse_currency_ref) as mongo:
        chaos_equiv = _get_chaos_equiv(mongo)["info"]
        new_entries = []
        for currency in currencies:
            currency_info = chaos_equiv[currency] if currency in chaos_equiv else None
            poe_official_currency = currency_ref[currency]["id"]
            if currency == "Chaos Orb":
                currency_info = {
                    "sell_price": 1000,
                    "sell_listings": 1000,
                }
            sell_price = (
                currency_info["sell_price"] if currency_info is not None else None
            )
            sell_listings = (
                currency_info["sell_listings"] if currency_info is not None else None
            )
            if sell_price and sell_listings > 15:
                new_entries.append(
                    asyncio.run(
                        poe_official.get_trades(
                            poe_official_currency, poe_official_currencies, DELAY
                        )
                    )
                )
            elapsed_time += (len(currencies) - 1) * DELAY
            print(
                f"Added {currency} to new entries, {round((total_time - elapsed_time)/60, 2)} minutes remaining"
            )
        mongo.insert_entries(new_entries)
        log = ""
        for entry in new_entries:
            log += f"{json.dumps(entry)} \n"
        return chaos_equiv
