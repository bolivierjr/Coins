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
        try:
            url = requests.get('https://api.coinbase.com/v2/'
                               'prices/ETH-USD/spot')
            res = url.json()
            price = str(res['data']['amount'])
            irc.reply('1 ETH (Ethereum) :: {0} USD'.format(price))

        except KeyError:
            irc.replay('Error: Please tell eck0 to MAEK FEEKS!')

    eth = wrap(eth)

    def btc(self, irc, msg, args):
        """takes no arguments

        Returns the pricing for BTC.
        """
        try:
            url = requests.get('https://api.coinbase.com/v2/'
                               'prices/BTC-USD/spot')
            res = url.json()
            price = str(res['data']['amount'])
            irc.reply('1 BTC (Bitcoin) :: {0} USD'.format(price))

        except KeyError:
            irc.reply('Error: Please tell eck0 to MAEK FEEKS!')
    btc = wrap(btc)

    def ltc(self, irc, msg, args):
        """takes no arguments

        Returns the pricing for LTC.
        """
        try:
            url = requests.get('https://api.coinbase.com/v2/'
                               'prices/LTC-USD/spot')
            res = url.json()
            price = str(res['data']['amount'])
            irc.reply('1 LTC (Litecoin) :: {0} USD'.format(price))

        except KeyError:
            irc.reply('Error: Please tell eck0 to MAEK FEEKS!')

    ltc = wrap(ltc)

    def zec(self, irc, msg, args):
        """takes no arguments

        Returns the pricing for ZEC.
        """
        try:
            url = requests.get('https://api.coinmarketcap.com/v1/'
                               'ticker/zcash')
            response = url.json()
            res = response[0]

            # Takes the string from repsonse and converts to a float and rounds
            # off two decimal points and converts it back to a string
            price = str(round(float(res['price_usd']), 2))
            irc.reply('1 {0} ({1}) :: {2} USD'
                      .format(res['symbol'], res['name'], price))

        except KeyError:
            irc.reply('Error: Please tell eck0 to MAEK FEEKS!')

    zec = wrap(zec)

    def sc(self, irc, msg, args):
        """takes no arguments

        Returns the pricing for ZEC.
        """
        try:
            url = requests.get('https://api.coinmarketcap.com/v1/'
                               'ticker/siacoin')
            response = url.json()
            res = response[0]

            # Takes the string from repsonse and converts to a float and rounds
            # off two decimal points and converts it back to a string
            price = str(round(float(res['price_usd']), 5) * 1000)
            irc.reply('1000 {0} ({1}) :: {2} USD'
                      .format(res['symbol'], res['name'], price))

        except KeyError:
            irc.reply('Error: Please tell eck0 to MAEK FEEKS!')

    sc = wrap(sc)

    def coin(self, irc, msg, args, text):
        """<symbol>
        Returns the pricing for the coin given in the 3 letter symbol argument.
        """
        try:
            url = requests.get('https://api.coinmarketcap.com/v1/ticker')
            response = url.json()

            def test():
                for res in response:
                    price = res['price_usd']
                    symbol = res['symbol']
                    name = res['name']
                    # Takes the string from repsonse and converts to a float
                    # and rounds off two decimal places and converts it back to
                    # a string if above a dollar
                    roundedPrice = str(round(float(price), 2))

                    if res['symbol'] == text.upper():
                        if float(price) < 0.01:
                            # Rounds 4 decimal places if below $0.01
                            roundedPrice = str(round(float(price), 4))
                            irc.reply('1 {0} ({1}) :: {2} USD'
                                      .format(symbol, name, roundedPrice))
                            return False
                        elif float(price) < 1:
                            # Rounds 3 decimal places if below $1.00
                            roundedPrice = str(round(float(price), 3))
                            irc.reply('1 {0} ({1}) :: {2} USD'
                                      .format(symbol, name, roundedPrice))
                            return False
                        elif float(price) >= 1:
                            irc.reply('1 {0} ({1}) :: {2} USD'
                                      .format(symbol, name, roundedPrice))
                            return False

                return True

            if test() is False:
                return
            else:
                irc.reply('Can\'t find {0} in the API, sorry.'
                          .format(text.upper()))

        except KeyError:
            irc.reply('Error: Please tell eck0 to MAEK FEEKS!')

    coin = wrap(coin, ['text'])


Class = Coins

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
