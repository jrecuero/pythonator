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

        >>> inst.attrDeps
        {}

        >>> inst.attrInDeps
        {}

        :type theName: str
        :param theName: Name of the instance
        """
        self.name        = theName
        """
        :type: str

        Instance name
        """

        self.state       = State.NONE
        """
        :type: State

        Instance state
        """

        self.instDeps    = plist.PList(Priority.PRIOS, Priority.DEFAULT)
        """
        :type: plist.PList

        Priority list with all instance dependencies
        """

        self.instInDeps  = plist.PList(Priority.PRIOS, Priority.DEFAULT)
        """
        :type: plist.Plist

        Priority list with all dependencies where instance is a dependency
        """

        self.attrDeps    = {}
        """
        :type: dict

        Dictionary with all instance-attribute pairs instance has a dependency
        """

        self.attrInDeps  = {}
        """
        :type: dict

        Dictionary with all instance attributes are in a dependency
        """

        self.stateTriggers = {}
        """
        :type: list

        List with all state triggers to be called when instance change state
        """

        self.attrTriggers = {}
        """
        :type: dict

        Dictionary with all attribute triggers to be called when attribute is
        updated
        """

        for st in State.ALL:
            self.stateTriggers[st] = None

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
    def addAttributeDependency(self, theDepAttr, ):
        """ Add dependency attribute id for an instance

        >>> inst = Instance('INSTANCE')
        >>> from depForAttribute import DepForAttribute
        >>> depForAttr = DepForAttribute(1, 'INSTANCE', 'OTHER', 'a', True)

        >>> inst.addAttributeDependency(depForAttr)
        True

        >>> ('OTHER', 'a') in inst.attrDeps
        True

        >>> inst.attrDeps[('OTHER', 'a')].getAllLists()
        [[], [1], []]

        :type theDepAttr: DepForAttribute
        :param theDepAttr: DepForAttributeInstance
        """
        if (theDepAttr.instDep, theDepAttr.attr) not in self.attrDeps:
            self.attrDeps[(theDepAttr.instDep, theDepAttr.attr)] = plist.PList(Priority.PRIOS, Priority.DEFAULT)
        self.attrDeps[(theDepAttr.instDep, theDepAttr.attr)].addAtFront(theDepAttr.id)
        return True

    # =========================================================================
    def removeAttributeDependency(self, theDepAttr):
        """ Remove dependency attribute id for an instance

        >>> inst = Instance('INSTANCE')
        >>> from depForAttribute import DepForAttribute
        >>> depForAttr = DepForAttribute(1, 'INSTANCE', 'OTHER', 'a', True)
        >>> inst.addAttributeDependency(depForAttr)
        True

        >>> inst.removeAttributeDependency(depForAttr)
        True

        :type theDepAttr: DepForAttribute
        :param theDepAttr: DepForAttributeInstance
        """
        if (theDepAttr.instDep, theDepAttr.attr) in self.attrDeps:
            self.attrDeps[(theDepAttr.instDep, theDepAttr.attr)].remove(theDepAttr.id)
        else:
            return False
        return True

    # =========================================================================
    def addAttributeInDependency(self, theDepAttr):
        """ Add dependency attribute id in the attribute instance

        >>> inst = Instance('INSTANCE')
        >>> from depForAttribute import DepForAttribute
        >>> depForAttr = DepForAttribute(1, 'INSTANCE', 'OTHER', 'a', True)

        >>> inst.addAttributeInDependency(depForAttr)
        True

        >>> 'a' in inst.attrInDeps
        True

        >>> inst.attrInDeps['a'].getAllLists()
        [[], [1], []]

        :type theDepAttr: DepForAttribute
        :param theDepAttr: DepForAttributeInstance
        """
        if not theDepAttr.attr in self.attrInDeps:
            self.attrInDeps[theDepAttr.attr] = plist.PList(Priority.PRIOS, Priority.DEFAULT)
        self.attrInDeps[theDepAttr.attr].addAtFront(theDepAttr.id)
        return True

    # =========================================================================
    def removeAttributeInDependency(self, theDepAttr):
        """ Remove dependency attribute id for in the attribute instance


        >>> inst = Instance('INSTANCE')
        >>> from depForAttribute import DepForAttribute
        >>> depForAttr = DepForAttribute(1, 'INSTANCE', 'OTHER', 'a', True)
        >>> inst.addAttributeInDependency(depForAttr)
        True

        >>> inst.removeAttributeInDependency(depForAttr)
        True

        :type theDepAttr: DepForAttribute
        :param theDepAttr: DepForAttributeInstance
        """
        if theDepAttr.attr in self.attrInDeps:
            self.attrInDeps[theDepAttr.attr].remove(theDepAttr.id)
        else:
            return False
        return True


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
