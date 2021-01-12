from flask import Response
from server.index import app
import requests
import asyncio
import json
from server.models.api_calls import POEOfficial, POENinja
from db.controller import Mongo
from server.controllers.api import update_listings, get_api_call_info
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
    api = POEOfficial("placeholder", "Standard")
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


@app.route("/api/v1/currency/params")
def time_estimate():
    api_call_info = get_api_call_info()
    api_call_info["time_estimate_minutes"] = round(api_call_info["time_estimate"] / 60, 2)
    del api_call_info['time_estimate']
    return Response(json.dumps(api_call_info), mimetype="text/json")


@app.route("/api/v1/currency")
def call_update_listings():
    update_listings()
    return "Finished", 200

@app.route("/api/v1/static")
def static_info():
    with Mongo() as mongo:
        static_info = mongo.get_static_info()
        if len(static_info):
            api = POEOfficial("placeholder", "Heist")
            mongo.insert_static_info(asyncio.run(api.get_currency_ref()))
            return mongo.get_static_info()
        return Response(static_info, mimetype="text/json")


@app.route("/api/v1/graph")
def return_graph():
    with Mongo() as mongo:
        graph = Graph(json.loads(mongo.find_currency()))
        # graph.get_profitable_trades("Chaos Orb")
        # return graph.print()
        # return json.dumps(graph.get_profitable_trades("Chaos Orb")["solutions"])
        return Response(json.dumps(graph.get_trades_profit("Chaos Orb")[0:30]), mimetype="text/json")
        # return Response(json.dumps(graph.get_trades_profit("Chaos Orb")), mimetype="text/json")

