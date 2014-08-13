#!/usr/bin/env python

"""info.py contains common helper methods.

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
import sys
import os

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
def FILE(backStep=0):
    """Return the name of the filename for the running function.

    It looks in the stack level, and return the name of the filename for the
    function running in the stack position for the given backward step.

    >>> def say(level=2):
    ...     print FILE(level)
    >>> say()
    /usr/lib/python2.7/doctest.py

    :type backStep: int
    :param backStep:
        Back steps to look in the stack.

    :rtype: string
    :return:
        Filename for the running function at the given stack position.
    """
    return sys._getframe(backStep + 1).f_code.co_filename


# ===========================================================================
def FUNC(backStep=0):
    """Return the name for the running function.

    It looks in the stack level, and return the name of the function running
    in the stack position for the given backward step.

    >>> def say(level=0):
    ...     print FUNC(level)
    >>> say()
    say

    >>> say(1)
    <module>

    >>> say(2)
    __run

    >>> say(3)
    run

    :type backStep: int
    :param backStep:
        Back steps to look in the stack.

    :rtype: string
    :return:
        Funtion name running at the given stack position.
    """
    return sys._getframe(backStep + 1).f_code.co_name


# ===========================================================================
def WHERE(backStep=0):
    """Return filename, line number and function name running at the given
    number of backward steps.

    >>> def say(level=0):
    ...     print WHERE(level)
    >>> say()
    <doctest __main__.WHERE[0]>/2 say()

    >>> say(1)
    <doctest __main__.WHERE[2]>/1 <module>()

    :type backStep: int
    :param backStep:
        Number of backward steps to look in the stack.

    :rtype: string
    :return:
        Full information about filename, line number and function running
        at the given backward steps in the stack.
    """
    frame = sys._getframe(backStep + 1)
    return "%s/%s %s()" % (os.path.basename(frame.f_code.co_filename),
                           frame.f_lineno, frame.f_code.co_name)


# ===========================================================================
def STACK(backStep=1):
    """Prints function in the stack for the given backward steps.

    >>> def say(level=0):
    ...     print STACK(level)
    >>> say()
    STACK
    say
    <module>
    __run
    run
    testmod
    <module>
    None

    >>> say(1)
    say
    <module>
    __run
    run
    testmod
    <module>
    None

    >>> say(2)
    <module>
    __run
    run
    testmod
    <module>
    None

    :type backStep: int
    :param backStep:
        Number of backward steps to look in the stack.
    """
    while True:
        try:
            print FUNC(backStep)
            backStep += 1
        except:
            return


#       _                     _       __ _       _ _   _
#   ___| | __ _ ___ ___    __| | ___ / _(_)_ __ (_) |_(_) ___  _ __  ___
#  / __| |/ _` / __/ __|  / _` |/ _ \ |_| | '_ \| | __| |/ _ \| '_ \/ __|
# | (__| | (_| \__ \__ \ | (_| |  __/  _| | | | | | |_| | (_) | | | \__ \
#  \___|_|\__,_|___/___/  \__,_|\___|_| |_|_| |_|_|\__|_|\___/|_| |_|___/
#
#############################################################################
#


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
