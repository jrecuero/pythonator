#!/usr/bin/env python

""" instance.py contains class Instance, which is the dependator instance.

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
import plist
from state import State
from priority import Priority


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
class Instance(object):
    """ Class were instance are stored
    """

    # =========================================================================
    def __init__(self, theName):
        """ Instance initialization

        >>> inst = Instance('INSTANCE')

        >>> inst.name
        'INSTANCE'

        >>> inst.state
        0

        >>> inst.instDeps # doctest: +ELLIPSIS
        <plist.PList object at 0x...>

        >>> inst.instDeps.getAllLists()
        [[], [], []]

        >>> inst.instDeps.priorityValues.getList()
        (1, 2, 3)

        >>> inst.instDeps.priorityValues.getDefault()
        2

        >>> inst.instInDeps # doctest: +ELLIPSIS
        <plist.PList object at 0x...>

        >>> inst.instInDeps.getAllLists()
        [[], [], []]

        >>> inst.instInDeps.priorityValues.getList()
        (1, 2, 3)

        >>> inst.instInDeps.priorityValues.getDefault()
        2

        >>> inst.attrDeps # doctest: +ELLIPSIS
        <plist.PList object at 0x...>

        >>> inst.attrDeps.getAllLists()
        [[], [], []]

        >>> inst.attrDeps.priorityValues.getList()
        (1, 2, 3)

        >>> inst.attrDeps.priorityValues.getDefault()
        2

        >>> inst.attrInDeps # doctest: +ELLIPSIS
        <plist.PList object at 0x...>

        >>> inst.attrInDeps.getAllLists()
        [[], [], []]

        >>> inst.attrInDeps.priorityValues.getList()
        (1, 2, 3)

        >>> inst.attrInDeps.priorityValues.getDefault()
        2

        :type theName: str
        :param theName: Name of the instace
        """
        self.name        = theName
        self.state       = State.NONE
        self.instDeps    = plist.PList(Priority.PRIOS, Priority.DEFAULT)
        self.instInDeps  = plist.PList(Priority.PRIOS, Priority.DEFAULT)
        self.attrDeps    = plist.PList(Priority.PRIOS, Priority.DEFAULT)
        self.attrInDeps  = plist.PList(Priority.PRIOS, Priority.DEFAULT)
        self.triggers    = {}
        for st in State.ALL:
            self.triggers[st] = None

    # =========================================================================
    def addInstanceDependency(self, theInstID):
        """
        """
        self.instDeps.addAtFront(theInstID)

    # =========================================================================
    def addInstanceInDependency(self, theInstID):
        """
        """
        self.instInDeps.addAtFront(theInstID)


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
