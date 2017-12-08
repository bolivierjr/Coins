#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017, Bruce Olivier
# All rights reserved.

import json
import requests
import supybot.utils as utils
import supybot.commands as commands
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Coins')
except ImportError:
    """
    Placeholder that allows to run the plugin on a bot
    without the i18n module
    """
    def _(x): return x


class Coins(callbacks.Plugin):
    threaded = True
    messages = {
        'httpErr': 'Sorry, there seems to be a problem with the API - {0}',
        'error': 'Error: Please tell eck0 to MAEK FEEKS!',
        'tooManyErr': 'Too many requests. Calm down!'
    }

    def _init_(self, irc):
        self.__parent = super(Coins, self)
        self.__parent.__init__(irc)

    def coinbase(self, irc, msg, args):
        """takes no arguments
        Returns the pricing for BTC, ETH, & LTC coins.
        """
        coins = ['BTC', 'ETH', 'LTC']
        prices = []
        message = Coins.messages

        try:
            for coin in coins:
                url = requests.get('https://api.coinbase.com/v2/prices/{0}-USD/spot'.format(coin))
                url.raise_for_status()
                res = url.json()
                price = str(res.get('data').get('amount'))
                symbol = res.get('data').get('base')
                prices.append('{0} - {1} USD'.format(symbol, price))
            irc.reply(' :: '.join(prices))

        except requests.exceptions.HTTPError as e:
            err = str(e)
            if err.startswith('429'):
                irc.reply(message.get('tooManyErr'))
            else:
                irc.reply(message.get('httpErr').format(str(err[:3])))

        except AttributeError:
            irc.reply(message.get('error'))

    coinbase = commands.wrap(coinbase)

    def eth(self, irc, msg, args):
        """takes no arguments
        Returns the pricing for ETH.
        """

        message = Coins.messages

        try:
            url = requests.get('https://api.coinbase.com/v2/prices/ETH-USD/spot')
            url.raise_for_status()
            res = url.json()
            price = str(res.get('data').get('amount'))
            irc.reply('1 ETH (Ethereum) :: {0} USD'.format(price))

        except requests.exceptions.HTTPError as e:
            err = str(e)
            if err.startswith('429'):
                irc.reply(message.get('tooManyErr'))
            else:
                irc.reply(message.get('httpErr').format(err[:3]))

        except AttributeError:
            irc.reply(message.get('error'))

    eth = commands.wrap(eth)

    def btc(self, irc, msg, args):
        """takes no arguments
        Returns the pricing for BTC.
        """

        message = Coins.messages

        try:
            url = requests.get('https://api.coinbase.com/v2/prices/BTC-USD/spot')
            url.raise_for_status()
            res = url.json()
            price = str(res.get('data').get('amount'))
            irc.reply('1 BTC (Bitcoin) :: {0} USD'.format(price))

        except requests.exceptions.HTTPError as e:
            err = str(e)
            if err.startswith('429'):
                irc.reply(message.get('tooManyErr'))
            else:
                irc.reply(message.get('httpErr').format(err[:3]))

        except AttributeError:
            irc.reply(message.get('error'))

        except ValueError as e:
            irc.reply(e)

    btc = commands.wrap(btc)

    def ltc(self, irc, msg, args):
        """takes no arguments
        Returns the pricing for LTC.
        """

        message = Coins.messages

        try:
            url = requests.get('https://api.coinbase.com/v2/prices/LTC-USD/spot')
            res = url.json()
            url.raise_for_status()
            price = str(res.get('data').get('amount'))
            irc.reply('1 LTC (Litecoin) :: {0} USD'.format(price))

        except requests.exceptions.HTTPError as e:
            err = str(e)
            if err.startswith('429'):
                irc.reply(message.get('tooManyErr'))
            else:
                irc.reply(message.get('httpErr').format(err[:3]))

        except AttributeError:
            irc.reply(message.get('error'))

        except ValueError as e:
            irc.reply(e)

    ltc = commands.wrap(ltc)

    def zec(self, irc, msg, args):
        """takes no arguments
        Returns the pricing for ZEC.
        """

        message = Coins.messages

        try:
            url = requests.get('https://api.coinmarketcap.com/v1/ticker/zcash')
            url.raise_for_status()
            response = url.json()
            res = response[0]
            symbol = res.get('symbol')
            name = res.get('name')
            price = float(res.get('price_usd'))

            irc.reply('1 {0} ({1}) :: {2} USD'.format(symbol, name,
                      '{0:.2f}'.format(price)))

        except requests.exceptions.HTTPError as e:
            err = str(e)
            if err.startswith('429'):
                irc.reply(message.get('tooManyErr'))
            else:
                irc.reply(message.get('httpErr').format(err[:3]))

        except TypeError:
            irc.reply(message.get('error'))

        except ValueError as e:
            irc.reply(e)

    zec = commands.wrap(zec)

    def sc(self, irc, msg, args):
        """takes no arguments
        Returns the pricing for ZEC.
        """

        message = Coins.messages

        try:
            url = requests.get('https://api.coinmarketcap.com/v1/'
                               'ticker/siacoin')
            url.raise_for_status()
            response = url.json()
            res = response[0]
            symbol = res.get('symbol')
            name = res.get('name')
            price = (float(res.get('price_usd')) * 1000)

            irc.reply('1000 {0} ({1}) :: {2} USD'.format(symbol, name, '{0:.2f}'.format(price)))

        except requests.exceptions.HTTPError as e:
            err = str(e)

            if err.startswith('429'):
                irc.reply(message.get('tooManyErr'))
            else:
                irc.reply(message.get('httpErr').format(err[:3]))

        except TypeError:
            irc.reply(message.get('error'))

        except ValueError as e:
            irc.reply(e)

    sc = commands.wrap(sc)

    def coin(self, irc, msg, args, text):
        """<symbol>
        Returns the pricing for the coin given in the 3 letter symbol argument.
        """

        message = Coins.messages

        try:
            url = requests.get('https://api.coinmarketcap.com/v1/ticker')
            url.raise_for_status()
            response = url.json()

            for res in response:
                price = float(res.get('price_usd'))
                symbol = res.get('symbol')
                name = res.get('name')

                if symbol == text.upper():
                    if price < 0.01:
                        # Rounds 4 decimal places if below $0.01
                        irc.reply('1 {0} ({1}) :: {2} USD'.format(symbol, name, '{0:.4f}'.format(price)))
                        break
                    elif price < 1:
                        # Rounds 3 decimal places if below $1.00
                        irc.reply('1 {0} ({1}) :: {2} USD'.format(symbol, name, '{0:.3f}'.format(price)))
                        break
                    elif price >= 1:
                        # Rounds 2 decimal places for everything else
                        irc.reply('1 {0} ({1}) :: {2} USD'.format(symbol, name, '{0:.2f}'.format(price)))
                        break
            else:
                irc.reply('Can\'t find {0} in the API, sorry.'
                          .format(text.upper()))

        except requests.exceptions.HTTPError as e:
            err = str(e)
            if err.startswith('429'):
                irc.reply(message.get('tooManyErr'))
            else:
                irc.reply(message.get('httpErr').format(err[:3]))

        except TypeError:
            irc.reply(message.get('error'))

        except ValueError as e:
            irc.reply(e)

    coin = commands.wrap(coin, ['text'])


Class = Coins

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
