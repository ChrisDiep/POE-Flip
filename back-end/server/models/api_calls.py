import aiohttp
import json
from time import sleep
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
        self.currency_ref_url = "https://www.pathofexile.com/api/trade/data/static"

    def _generate_trade_url(self, trade_ids, query):
        item_id_str = ",".join(trade_ids)
        url = self.trades_url + (f"{item_id_str}?query={query}&exchange")
        return url

    async def get_currency_ref(self):
        async with Requests() as connection:
            response = await connection.get(url=self.currency_ref_url)
            return response

    async def get_trade(self, have, want):
        """ Get the trade listing information given the buy/sell currency """
        payload = {
            "exchange": {"status": {"option": "online"}, "have": [have], "want": [want]}
        }
        async with Requests() as connection:
            trade_info = await connection.post(url=self.trade_id_url, json=payload)
            if len(trade_info["result"]) != 0:
                url = self._generate_trade_url(
                    trade_info["result"][0:10], trade_info["id"]
                )
                trades = await connection.get(url=url)
                return trades
            return None

    async def get_trades(self, have, wants, delay):
        """ Get Multiple Buy Offers for One Currency """
        results = []
        for want in wants:
            if have != want:
                sleep(delay)
                print(f"Requesting: {want} for {have}")
                request = self.get_trade(have, want)
                results.append(request)
        return await asyncio.gather(*results)
        # return None


class POENinja:
    def __init__(self, curr_league):
        self.league = curr_league
        self.currency_url = f"https://poe.ninja/api/data/CurrencyOverview?league={self.league}&type=Currency&language=en"

    async def get_currencies(self):
        async with Requests() as connection:
            currencies = await connection.get(url=self.currency_url)
            return currencies


# currencies = [
#     "exalted",
#     "chaos",
#     "divine",
# ]

# api = POEOfficial("placeholder", "Heist")
# print(asyncio.run(api.get_trades("chaos", currencies)))
