###
# Copyright (c) 2017, Bruce Olivier
# All rights reserved.
#
#
###
import json
import requests
import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Coins')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    def _(x): return x


class Coins(callbacks.Plugin):
    threaded = True

    def _init_(self, irc):
        self.__parent = super(Coins, self)
        self.__parent.__init__(irc)

    def _init_(self, irc):
        self.__parent = super(Coins, self)
        self.__parent.__init__(irc)

    def coinbase(self, irc, msg, args):
        """takes no arguments

        Returns the pricing for BTC, ETH, & LTC.
        """
        coins = ['BTC', 'ETH', 'LTC']
        response = []
        prices = []

        try:
            for coin in coins:
                url = requests.get('https://api.coinbase.com/v2/prices/{0}-USD'
                                   '/spot'.format(coin))
                res = url.json()
                response.append(res)
                price = str(res['data']['amount'])
                symbol = res['data']['base']
                prices.append('{0} - {1} USD'.format(symbol, price))

            irc.reply(' :: '.join(prices))

        except KeyError:
            irc.reply('Error: Please tell eck0 to MAEK FEEKS!')

    coinbase = wrap(coinbase)

    def eth(self, irc, msg, args):
        """takes no arguments

        Returns the pricing for ETH.
        """
        url = requests.get('https://api.coinbase.com/v2/prices/ETH-USD/spot')
        res = url.json()
        price = str(res['data']['amount'])
        irc.reply('1 ETH (Ethereum) :: {0} USD'.format(price))
    eth = wrap(eth)

    def btc(self, irc, msg, args):
        """takes no arguments

        Returns the pricing for BTC.
        """
        url = requests.get('https://api.coinbase.com/v2/prices/BTC-USD/spot')
        res = url.json()
        price = str(res['data']['amount'])
        irc.reply('1 BTC (Bitcoin) :: {0} USD'.format(price))
    btc = wrap(btc)

    def ltc(self, irc, msg, args):
        """takes no arguments

        Returns the pricing for LTC.
        """
        url = requests.get('https://api.coinbase.com/v2/prices/LTC-USD/spot')
        res = url.json()
        price = str(res['data']['amount'])
        irc.reply('1 LTC (Litecoin) :: {0} USD'.format(price))
    ltc = wrap(ltc)

    def zec(self, irc, msg, args):
        """takes no arguments

        Returns the pricing for ZEC.
        """
        url = requests.get('https://api.coinmarketcap.com/v1/ticker/zcash')
        response = url.json()
        res = response[0]

        # Takes the string from repsonse and converts to a float and rounds off
        # two decimal points and converts it back to a string
        price = str(round(float(res['price_usd']), 2))
        irc.reply('1 {0} ({1}) :: {2} USD'
                  .format(res['symbol'], res['name'], price))
    zec = wrap(zec)

    def sc(self, irc, msg, args):
        """takes no arguments

        Returns the pricing for ZEC.
        """
        url = requests.get('https://api.coinmarketcap.com/v1/ticker/siacoin')
        response = url.json()
        res = response[0]

        # Takes the string from repsonse and converts to a float and rounds off
        # two decimal points and converts it back to a string
        price = str(round(float(res['price_usd']), 5) * 1000)
        irc.reply('1000 {0} ({1}) :: {2} USD'
                  .format(res['symbol'], res['name'], price))
    sc = wrap(sc)

    def coin(self, irc, msg, args, text):
        """<symbol>
        Returns the pricing for the coin given in the 3 letter symbol argument.
        """
        url = requests.get('https://api.coinmarketcap.com/v1/ticker')
        response = url.json()

        for res in response:
            # Takes the string from repsonse and converts to a float and rounds
            # off two decimal places and converts it back to a string if above
            # a dollar
            price = str(round(float(res['price_usd']), 2))
            symbol = res['symbol']
            name = res['name']

            if res['symbol'] == text.upper():
                if float(res['price_usd']) < 0.01:
                    # Rounds 4 decimal places if below $0.01
                    price = str(round(float(res['price_usd']), 4))
                    irc.reply('1 {0} ({1}) :: {2} USD'
                              .format(symbol, name, price))
                    return
                elif float(res['price_usd']) < 1:
                    # Rounds 3 decimal places if below $1.00
                    price = str(round(float(res['price_usd']), 3))
                    irc.reply('1 {0} ({1}) :: {2} USD'
                              .format(symbol, name, price))
                    return

                irc.reply('1 {0} ({1}) :: {2} USD'.format(symbol, name, price))
    coin = wrap(coin, ['text'])


Class = Coins

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
