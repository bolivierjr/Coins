###
# Copyright (c) 2017, Bruce Olivier
# All rights reserved.
#
 
import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('EfnetQuotes')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x


class EfnetQuotes(callbacks.Plugin):
    """A list of channel quotes that you can add or remove and call randomly."""
    threaded = True


Class = EfnetQuotes


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
