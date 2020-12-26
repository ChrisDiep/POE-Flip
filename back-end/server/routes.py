from server.server import app
import requests
import asyncio
from server.models.api_calls import POEOfficial
from db.controller import Mongo


# @app.route("/")
# def index():
#     test = POEOfficial("123", "Heist")
#     # resp = await asyncio.run(test.asynctest())
#     print("here")
#     # return asyncio.run(test.asynctest2())
#     return asyncio.run(test.get_trade("exalted", "chaos"))

@app.route("/")
def hello():
    return "Hello"

@app.route('/api/v1/poeofficial/currency', methods=["GET"])
def return_top_trades():
    currencies = [
        "exalted-orb",
        "chaos",
        "divine",
        "fusing",
        "vaal-orb",
    ]
    api = POEOfficial("placeholder", "Heist")
    with Mongo() as mongo:
        db_entries = mongo.get_total_entries()
        # if (mongo.get_stale_entries()):
        #     #update stale entries
        #     print('not')
        # elif (db_entries != currencies.length):
        new_entries = []
        for currency in currencies:
            if currency not in db_entries:
                new_entries.append(asyncio.run(api.get_trades(currency, currencies)))
        mongo.insert_entries(new_entries)
        # else:
        #     #pull from db
        # return mongo.find()
        return "hello"