from server import app
import requests
import asyncio
from server.api_calls import POEOfficial


@app.route("/")
def index():
    test = POEOfficial("123", "Heist")
    # resp = await asyncio.run(test.asynctest())
    print("here")
    # return asyncio.run(test.asynctest2())
    return asyncio.run(test.get_trades("exalted", "chaos"))


# @app.route('/api/v1/poeofficial/currency', methods=["GET"])
# def return_currency():