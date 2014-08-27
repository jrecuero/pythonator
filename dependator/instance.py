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

        Every instance contains the instance name, the state for the instance
        and four lists:

        * List with IDs for all dependencies this instance have

        * List with IDs for all dependencies this instance is included

        * List with IDs for all attribute dependencies this instance have

        * List with IDs for all attribute dependencies this instance is
        included

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
        :param theName: Name of the instance
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
    def addInstanceDependency(self, theInstId):
        """ Add dependency id for an instance

        Add the id for dependencies for the given instance. It can search in
        that all dependencies for the given instance

        >>> inst = Instance('INSTANCE')

        >>> inst.addInstanceDependency(1)
        1

        >>> inst.instDeps.getAllLists()
        [[], [1], []]

        :type theInstId: int
        :param theInstId: Id for the dependecy

        :rtype: int
        :return: instance id added
        """
        return self.instDeps.addAtFront(theInstId)

    # =========================================================================
    def removeInstanceDependency(self, theInstId):
        """ Remove dependency id for an instance

        Remove the id for dependencies for the given instance.

        >>> inst = Instance('INSTANCE')
        >>> inst.addInstanceDependency(1)
        1
        >>> inst.instDeps.getAllLists()
        [[], [1], []]

        >>> inst.removeInstanceDependency(1)
        1

        >>> inst.instDeps.getAllLists()
        [[], [], []]

        :type theInstId: int
        :param theInstId: Id for the dependecy

        :rtype: int
        :return: instance id removed else None if not found
        """
        return self.instDeps.remove(theInstId)

    # =========================================================================
    def addInstanceInDependency(self, theInstId):
        """ Add in dependecy id for an instance

        Instance is in the given dependency as a dependency, so the id is
        stored in order to check when instance state change what other
        instances should be notified

        >>> inst = Instance('INSTANCE')

        >>> inst.addInstanceInDependency(1)
        1

        >>> inst.instInDeps.getAllLists()
        [[], [1], []]

        :type theInstId: int
        :param theInstId: Id for the dependecy

        :rtype: int
        :return: instance id added
        """
        return self.instInDeps.addAtFront(theInstId)

    # =========================================================================
    def removeInstanceInDependency(self, theInstId):
        """ Remove dependency id for an instance

        Remove the id for dependencies for the given instance.

        >>> inst = Instance('INSTANCE')
        >>> inst.addInstanceInDependency(1)
        1
        >>> inst.instInDeps.getAllLists()
        [[], [1], []]

        >>> inst.removeInstanceInDependency(1)
        1

        >>> inst.instInDeps.getAllLists()
        [[], [], []]

        :type theInstId: int
        :param theInstId: Id for the dependecy

        :rtype: int
        :return: instance id removed else None if not found
        """
        return self.instInDeps.remove(theInstId)

    # =========================================================================
    def addAttributeDependency(self, theAttrId):
        """ Add dependency attribute id for an instance

        >>> inst = Instance('INSTANCE')

        >>> inst.addAttributeDependency(1)
        1

        >>> inst.attrDeps.getAllLists()
        [[], [1], []]

        :type theAttrId: int
        :param theAttrId: Id for the attribute
        """
        return self.attrDeps.addAtFront(theAttrId)

    # =========================================================================
    def removeAttributeDependency(self, theAttrId):
        """ Remove dependency attribute id for an instance

        >>> inst = Instance('INSTANCE')
        >>> inst.addAttributeDependency(1)
        1
        >>> inst.attrDeps.getAllLists()
        [[], [1], []]

        >>> inst.removeAttributeDependency(1)
        1

        >>> inst.attrDeps.getAllLists()
        [[], [], []]

        :type theAttrId: int
        :param theAttrId: Id for the attribute
        """
        return self.attrDeps.remove(theAttrId)

    # =========================================================================
    def addAttributeInDependency(self, theAttrId):
        """ Add dependency attribute id in the attribute instance

        >>> inst = Instance('INSTANCE')

        >>> inst.addAttributeInDependency(1)
        1

        >>> inst.attrInDeps.getAllLists()
        [[], [1], []]

        :type theAttrId: int
        :param theAttrId: Id for the attribute
        """
        return self.attrInDeps.addAtFront(theAttrId)

    # =========================================================================
    def removeAttributeInDependency(self, theAttrId):
        """ Remove dependency attribute id for in the attribute instance

        >>> inst = Instance('INSTANCE')
        >>> inst.addAttributeInDependency(1)
        1
        >>> inst.attrInDeps.getAllLists()
        [[], [1], []]

        >>> inst.removeAttributeInDependency(1)
        1

        >>> inst.attrInDeps.getAllLists()
        [[], [], []]

        :type theAttrId: int
        :param theAttrId: Id for the attribute
        """
        return self.attrInDeps.remove(theAttrId)


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
