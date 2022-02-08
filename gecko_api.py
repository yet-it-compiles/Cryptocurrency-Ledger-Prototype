""" Simple module which retrieves the requested cryptocurrency information """

import requests
from PIL import Image
from io import BytesIO


class GeckoApi:
    crypto_name = ""

    def __init__(self, crypto_name):
        self.name = crypto_name

    def get_coin(self):
        """
        Returns the dictionary representation of the coin with all available attributes
        :rtype: dict
        :return requested_crypto_info: the queried coin dictionary
        """
        info_from_api = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids="
        json_converter = "&order=market_cap_desc&per_page=100&page=1&sparkline=false"
        requested_crypto_info = requests.get(info_from_api + self.name.lower() + json_converter).json()

        return requested_crypto_info

    def get_attribute(self, attribute):
        """
        Retrieves a specific attribute request
        Note: Users must enter name (not symbol), not case-sensitive.
        :param attribute: the given attribute (use any from Attributes table above)
        :type attribute: str
        :rtype: int | float | str
        :return: crypto_attribute[0][attribute]
        """
        crypto_attribute = self.get_coin()
        if crypto_attribute:
            return crypto_attribute[0][attribute]

    def get_icon(self):
        """
        Retrieves the image of the requested cryptocurrency
        :rtype: Image
        :return crypto_icon
        """
        crypto_image = self.get_coin()

        if crypto_image:
            crypto_image_url = crypto_image[0]["image"]  # captures the
            server_response = requests.get(crypto_image_url)
            image_bytes = BytesIO(server_response.content)
            crypto_icon = Image.open(image_bytes)
            return crypto_icon

    def get_ohlc_data(self, days_previous):
        """
        Returns a list of opening price, high/low, and closing price for the period
        :param days_previous: int
        :rtype: list
        :return: coin_ohlc
        """
        info_from_api = 'https://api.coingecko.com/api/v3/coins/'
        json_converter = '/ohlc?vs_currency=usd&days='

        coin_ohlc = requests.get(info_from_api + self.name.lower().strip() + json_converter + str(days_previous)).json()

        # return an empty list if the coin does not exist (api returns error dictionary)
        if type(coin_ohlc) == dict:
            coin_ohlc = []

        return coin_ohlc

    def get_price_history(self, days_previous, separate=False):
        """
        Returns a list of historical price data in the form of  [unix_timestamp, price]
        :param days_previous: int
        :param separate: bool
        :rtype: list
        :return: price_history
        """
        info_from_api = 'https://api.coingecko.com/api/v3/coins/'
        json_converter = '/market_chart?vs_currency=usd&days='
        price_history = requests.get(info_from_api + self.name.lower().strip() + json_converter + str(days_previous)).json()

        # return empty list if coin name is not recognized
        if "error" in price_history.keys():
            price_history = []
        else:
            price_history = price_history["prices"]

        # separate json dictionary into two lists
        if separate:
            times = []
            prices = []
            # only try to split if price_hist is non-empty
            if price_history:
                for item in price_history:
                    times.append(item[0])
                    prices.append(item[1])
            return times, prices
        else:
            return price_history

    def get_market_cap_history(self, days_previous, separate=False):
        """
        Returns a list of historical market cap data, each entry having the form: [unix_timestamp, market_cap]
        :param days_previous: int
        :param separate: bool
        :rtype: list
        :return: market_cap_hist
        """
        info_from_api = 'https://api.coingecko.com/api/v3/coins/'
        json_converter = '/market_chart?vs_currency=usd&days='
        market_cap_hist = requests.get(info_from_api + self.name.lower().strip() + json_converter +
                                       str(days_previous)).json()

        # return empty list if coin name is not recognized
        if "error" in market_cap_hist.keys():
            market_cap_hist = []
        else:
            market_cap_hist = market_cap_hist["market_caps"]

        if separate:
            times = []
            market_caps = []
            # only try to split if market_cap_hist is non-empty
            if market_cap_hist:
                for item in market_cap_hist:
                    times.append(item[0])
                    market_caps.append(item[1])
            return times, market_caps
        else:
            return market_cap_hist

    def get_volume_history(self, days_previous, separate=False):
        """
        Returns a list of historical total volume data, each entry having the form: [unix_timestamp, total_volume]
        :param days_previous: int
        :param separate: bool
        :rtype: list
        :return: total_volume_history
        """
        info_from_api = 'https://api.coingecko.com/api/v3/coins/'
        json_converter = '/market_chart?vs_currency=usd&days='
        total_volume_history = requests.get(info_from_api, self.crypto_name.lower().strip(), json_converter,
                                         str(days_previous)).json()

        # return empty list if coin name is not recognized
        if "error" in total_volume_history.keys():
            total_volume_history = []
        else:
            total_volume_history = total_volume_history["total_volumes"]

        if separate:
            times = []
            total_volumes = []
            # only try to split if total_volume_hist is non-empty
            if total_volume_history:
                for item in total_volume_history:
                    times.append(item[0])
                    total_volumes.append(item[1])
            return times, total_volumes
        else:
            return total_volume_history