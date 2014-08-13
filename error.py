#!/usr/bin/env python

"""error.py contains BaseException class to be used for custom exceptions.

:author:    Jose Carlos Recuero
:version:   0.1
:since:     08/13/2014

"""

__docformat__ = 'restructuredtext en'

##  _                            _
## (_)_ __ ___  _ __   ___  _ __| |_ ___
## | | '_ ` _ \| '_ \ / _ \| '__| __/ __|
## | | | | | | | |_) | (_) | |  | |_\__ \
## |_|_| |_| |_| .__/ \___/|_|   \__|___/
##             |_|
#############################################################################
#
# import std python modules
#

#
# import user python modules
#


#
#                      _              _
#   ___ ___  _ __  ___| |_ __ _ _ __ | |_ ___
#  / __/ _ \| '_ \/ __| __/ _` | '_ \| __/ __|
# | (_| (_) | | | \__ \ || (_| | | | | |_\__ \
#  \___\___/|_| |_|___/\__\__,_|_| |_|\__|___/
#
#############################################################################
#


#            _                     _   _
#  ___ _   _| |__  _ __ ___  _   _| |_(_)_ __   ___  ___
# / __| | | | '_ \| '__/ _ \| | | | __| | '_ \ / _ \/ __|
# \__ \ |_| | |_) | | | (_) | |_| | |_| | | | |  __/\__ \
# |___/\__,_|_.__/|_|  \___/ \__,_|\__|_|_| |_|\___||___/
#
#############################################################################
#

# ===========================================================================

#       _                     _       __ _       _ _   _
#   ___| | __ _ ___ ___    __| | ___ / _(_)_ __ (_) |_(_) ___  _ __  ___
#  / __| |/ _` / __/ __|  / _` |/ _ \ |_| | '_ \| | __| |/ _ \| '_ \/ __|
# | (__| | (_| \__ \__ \ | (_| |  __/  _| | | | | | |_| | (_) | | | \__ \
#  \___|_|\__,_|___/___/  \__,_|\___|_| |_|_| |_|_|\__|_|\___/|_| |_|___/
#
#############################################################################
#
class BaseException(Exception):
    """BaseException class allows custom exceptions.

    It allows derived exceptions with a default message and with additional
    customs message passed when the exception is raised.

    :type BASE_MESSAGE: string
    :cvar BASE_MESSAGE:
        Default exception message to be displayed when the exception is raised.
        It should be overrided by derived classes.
    """

    # =======================================================================
    BASE_MESSAGE = "Base Exception"

    # =======================================================================
    def __init__(self, customMessage="custom message"):
        """BaseException constructor.

        It construct a BaseException instance and it stores a custom message
        passed when the exception is created. This custom message will be
        displayed together with the default exception message.

        >>> ex = BaseException()

        >>> ex.BASE_MESSAGE
        'Base Exception'

        >>> ex.customMessage
        'custom message'

        >>> ex = BaseException('my exception')

        >>> ex.customMessage
        'my exception'

        :type customMessage: string
        :param customMessage:
            Custom message to be displayed then the exception is printed out.
        """
        self.customMessage = customMessage

    # =======================================================================
    def __str__(self):
        """Override __str__ method.

        >>> raise BaseException()
        Traceback (most recent call last):
        ...
        BaseException: Base Exception : custom message

        >>> raise BaseException('custom exception')
        Traceback (most recent call last):
        ...
        BaseException: Base Exception : custom exception

        It overrides __str__ in order to display default exception message
        and custom message.
        """
        return '%s : %s' % (self.BASE_MESSAGE, self.customMessage)


#                  _
#  _ __ ___   __ _(_)_ __
# | '_ ` _ \ / _` | | '_ \
# | | | | | | (_| | | | | |
# |_| |_| |_|\__,_|_|_| |_|
#
#############################################################################
#
if __name__ == "__main__":
    import doctest
    doctest.testmod()
