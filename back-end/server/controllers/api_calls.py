import aiohttp
import json

import asyncio

class Requests:
    """ Creates a shared client pool for requests """

    def __init__(self):
        self._session = aiohttp.ClientSession()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *err):
        await self._session.close()
        self._session = None

    async def get(self, **kwargs):
        """ General method for sending get requests using the shared pool """
        async with self._session.get(**kwargs) as resp:
            resp.raise_for_status()
            return await resp.json()

    async def post(self, **kwargs):
        """ General method for sending post requests using the shared pool """
        async with self._session.post(**kwargs) as resp:
            resp.raise_for_status()
            return await resp.json()


class POEOfficial:
    """ Requests for the Official Path of Exile Trade Site """

    def __init__(self, API_KEY, curr_league):
        self.API_KEY = API_KEY
        self.league = curr_league
        self.trade_id_url = (
            f"http://www.pathofexile.com/api/trade/exchange/{self.league}"
        )
        self.trades_url = "https://www.pathofexile.com/api/trade/fetch/"

    def _generate_trade_url(self, trade_ids, query):
        item_id_str = ",".join(trade_ids)
        url = self.trades_url + (f"{item_id_str}?query={query}&exchange")
        return url

    async def get_trade(self, have, want):
        """ Get the trade listing information given the buy/sell currency """
        payload = {
            "exchange": {"status": {"option": "online"}, "have": [have], "want": [want]}
        }
        async with Requests() as connection:
            trade_info = await connection.post(url=self.trade_id_url, json=payload)
            url = self._generate_trade_url(trade_info["result"][0:10], trade_info["id"])
            trades = await connection.get(url=url)
            return trades

    async def get_trades(self, have, wants):
        results = []
        for want in wants:
            if have != want:
                results.append(self.get_trade(have, want))
        return await asyncio.gather(*results)

# currencies = [
#     "exalted",
#     "chaos",
#     "divine",
# ]

# api = POEOfficial("placeholder", "Heist")
# print(asyncio.run(api.get_trades("chaos", currencies)))

