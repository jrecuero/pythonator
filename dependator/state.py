#!/usr/bin/env python

""" state.py contains class State, which is the dependator instance state

:author:    Jose Carlos Recuero
:version:   0.1
:since:     08/18/2014
"""

__docformat__ = 'restructuredtext en'

###############################################################################
##  _                            _
## (_)_ __ ___  _ __   ___  _ __| |_ ___
## | | '_ ` _ \| '_ \ / _ \| '__| __/ __|
## | | | | | | | |_) | (_) | |  | |_\__ \
## |_|_| |_| |_| .__/ \___/|_|   \__|___/
##             |_|
###############################################################################
#
# import std python modules
#

#
# import user defined python modules
#


###############################################################################
##
##   ___ ___  _ __  ___| |_ __ _ _ __ | |_ ___
##  / __/ _ \| '_ \/ __| __/ _` | '_ \| __/ __|
## | (_| (_) | | | \__ \ || (_| | | | | |_\__ \
##  \___\___/|_| |_|___/\__\__,_|_| |_|\__|___/
##
###############################################################################
#

###############################################################################
##            _                     _   _
##  ___ _   _| |__  _ __ ___  _   _| |_(_)_ __   ___  ___
## / __| | | | '_ \| '__/ _ \| | | | __| | '_ \ / _ \/ __|
## \__ \ |_| | |_) | | | (_) | |_| | |_| | | | |  __/\__ \
## |___/\__,_|_.__/|_|  \___/ \__,_|\__|_|_| |_|\___||___/
##
###############################################################################
#

###############################################################################
##       _                     _       __ _       _ _   _
##   ___| | __ _ ___ ___    __| | ___ / _(_)_ __ (_) |_(_) ___  _ __  ___
##  / __| |/ _` / __/ __|  / _` |/ _ \ |_| | '_ \| | __| |/ _ \| '_ \/ __|
## | (__| | (_| \__ \__ \ | (_| |  __/  _| | | | | | |_| | (_) | | | \__ \
##  \___|_|\__,_|___/___/  \__,_|\___|_| |_|_| |_|_|\__|_|\___/|_| |_|___/
##
###############################################################################
#

#
# =============================================================================
#
class State(object):
    """ Dependator instaces state.

    >>> State.NONE
    0

    >>> State.CREATED
    1

    >>> State.ACTIVED
    2

    >>> State.WAITING
    3

    >>> State.PAUSED
    4

    >>> State.DELETED
    5

    >>> State.ALL
    (0, 1, 2, 3, 4, 5)

    >>> State.NAMES
    ('NONE', 'CREATED', 'ACTIVED', 'WAITING', 'PAUSED', 'DELETED')

    """

    NONE    = 0
    """
    :type: int

    Instance None state. It is an unknown state
    """

    CREATED = 1
    """
    :type: int

    Instance Created state. This is the initial state in the life cycle
    """

    ACTIVED = 2
    """
    :type: int

    Instance Actived state.
    """

    WAITING = 3
    """
    :type: int

    Instance Waiting state.
    """

    PAUSED  = 4
    """
    :type: int

    Instance Paused state.
    """

    DELETED = 5
    """
    :type: int

    Instance Delete state. This is the last state in the life cycle
    """

    ALL = (NONE, CREATED, ACTIVED, WAITING, PAUSED, DELETED)
    """
    :type: tuple

    List with all possible states
    """

    NAMES = ('NONE', 'CREATED', 'ACTIVED', 'WAITING', 'PAUSED', 'DELETED')
    """
    :type: tuple

    List with all possible states
    """

###############################################################################
##                  _
##  _ __ ___   __ _(_)_ __
## | '_ ` _ \ / _` | | '_ \
## | | | | | | (_| | | | | |
## |_| |_| |_|\__,_|_|_| |_|
##
###############################################################################
#
if __name__ == "__main__":
    import doctest
    doctest.testmod()
