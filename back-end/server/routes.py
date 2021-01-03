from server.index import app
import requests
import asyncio
import json
from server.models.api_calls import POEOfficial, POENinja
from db.controller import Mongo
from server.controllers.api import update_listings, get_time_estimate_seconds
from server.models.graph import Graph
from server.models.sat_solver import *

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


@app.route("/api/v1/poeofficial/currency", methods=["GET"])
def return_top_trades():
    currencies = [
        "exalted-orb",
        "chaos",
        "divine",
        "fusing",
        "vaal-orb",
    ]
    api = POEOfficial("placeholder", "Heist")
    # Retrieve API Information
    # Traverse through Info to get top listings
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


@app.route("/api/v1/currency/time")
def time_estimate():
    obj = {"minutes": round(get_time_estimate_seconds() / 60, 2)}
    return json.dumps(obj)


@app.route("/api/v1/currency")
def call_update_listings():
    update_listings()
    return "Finished", 200

@app.route("/api/v1/static")
def static_info():
    with Mongo() as mongo:
        return mongo.get_static_info()


@app.route("/api/v1/graph")
def return_graph():
    with Mongo() as mongo:
        graph = Graph(json.loads(mongo.find_currency()))
        # graph.get_profitable_trades("Chaos Orb")
        # return graph.print()
        # return json.dumps(graph.get_profitable_trades("Chaos Orb")["solutions"])
        return json.dumps(graph.get_trades_profit("Chaos Orb"))
