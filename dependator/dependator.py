#!/usr/bin/env python

""" dependator.py contains class Dependator, which is the base implementation
for a dependency manager handler.

:author:    Jose Carlos Recuero
:version:   0.1
:since:     08/12/2014
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
#import plist
from state import State
#from priority import Priority
from instance import Instance
#from depForInstance import DepForInstance
#from depForAttribute import DepForAttribute


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
class Dependator(object):
    """ Dependator provides dependency manager handling.

    Any instance can be added to the dependator, every one is identified by a
    string name, that should be unique.

    Every instance has a state and two dictionaries: one with dependencies
    related with its status and other with dependencies related with its
    attributes.

    Attributes could be real attribute for the given instance or just logical
    attributes being handled by that instance.

    Instance state could be: None, Created, Actived, Waiting, Paused, Deleted.

    Every state has a set of notifications to be called when moving in or out
    that state.

    Attributes updates have a notification to be called when attribute is being
    updated.
    """

    # =========================================================================
    def __init__(self):
        """ Initialize dependator

        >>> dep = Dependator()

        >>> dep.instances # doctest: +ELLIPSIS
        {}

        """
        self.instances = {}
        """
        :type: dict

        It stores all instances registered to the dependator
        """

    # =========================================================================
    def registerInstance(self, theInstName):
        """ Register instance to dependator

        >>> dep = Dependator()

        >>> dep.registerInstance('THE_INSTANCE') # doctest: +ELLIPSIS
        <instance.Instance object at 0x...>

        >>> dep.instances # doctest: +ELLIPSIS
        {'THE_INSTANCE': <instance.Instance object at 0x...>}

        Second registration with the same name should not add any new entry
        >>> dep.registerInstance('THE_INSTANCE')

        >>> dep.instances # doctest: +ELLIPSIS
        {'THE_INSTANCE': <instance.Instance object at 0x...>}

        :type theInstName: str
        :param theInstName: Instance name to register
        """
        if theInstName in self.instances:
            return None
        instance = Instance(theInstName)
        self.instances[theInstName] = instance
        return instance

    # =========================================================================
    def deregisterInstance(self, theInstName):
        """ Deregister instance from the dependator
        >>> dep = Dependator()
        >>> dep.registerInstance('THE_INSTANCE') # doctest: +ELLIPSIS
        <instance.Instance object at 0x...>

        >>> instance = dep.deregisterInstance('THE_INSTANCE') # doctest: +ELLIPSIS
        >>> instance.name
        'THE_INSTANCE'

        Second deregistration with the same name should not remove any entry
        >>> instance = dep.deregisterInstance('THE_INSTANCE') # doctest: +ELLIPSIS
        >>> instance

        :type theInstName: str
        :param theInstName: Instance name to deregister
        """
        if theInstName in self.instances:
            instance = self.instances[theInstName]
            del self.instances[theInstName]
            return instance
        return None

    # =========================================================================
    def _setState(self, theInstName, theState):
        """ Change instance state to the given state

        >>> dep = Dependator()
        >>> instance = dep.registerInstance('INST')
        >>> instance.state
        0

        >>> dep._setState("NOT INST", State.CREATED)
        False

        >>> dep._setState("INST", State.CREATED)
        True
        >>> instance.state
        1

        >>> dep._setState("INST", State.ACTIVED)
        True
        >>> instance.state
        2

        >>> dep._setState("INST", State.WAITING)
        True
        >>> instance.state
        3

        >>> dep._setState("INST", State.PAUSED)
        True
        >>> instance.state
        4

        >>> dep._setState("INST", State.DELETED)
        True
        >>> instance.state
        5

        :type theInstName: str
        :param theInstName: Instance name to change state

        :type theState: State
        :param theState: New state to set the given instance
        """
        if theInstName in self.instances:
            instance = self.instances[theInstName]
            instance.state = theState
            return True
        return False

    # =========================================================================
    def notifyCreated(self, theInstName):
        """ Notify instance change to Created state

        >>> dep = Dependator()
        >>> instance = dep.registerInstance('THE_INSTANCE')
        >>> instance.state
        0

        >>> dep.notifyCreated("THE_INSTANCE")
        True
        >>> instance.state
        1

        :type theInstName: str
        :param theInstName: Instance name to change state
        """
        return self._setState(theInstName, State.CREATED)

    # =========================================================================
    def notifyActived(self, theInstName):
        """ Notify instance change to Actived state

        >>> dep = Dependator()
        >>> instance = dep.registerInstance('THE_INSTANCE')
        >>> instance.state
        0

        >>> dep.notifyActived("THE_INSTANCE")
        True
        >>> instance.state
        2

        :type theInstName: str
        :param theInstName: Instance name to change state
        """
        return self._setState(theInstName, State.ACTIVED)

    # =========================================================================
    def notifyWaiting(self, theInstName):
        """ Notify instance change to Waiting state

        >>> dep = Dependator()
        >>> instance = dep.registerInstance('THE_INSTANCE')
        >>> instance.state
        0

        >>> dep.notifyWaiting("THE_INSTANCE")
        True
        >>> instance.state
        3

        :type theInstName: str
        :param theInstName: Instance name to change state
        """
        return self._setState(theInstName, State.WAITING)

    # =========================================================================
    def notifyPaused(self, theInstName):
        """ Notify instance change to Paused state

        >>> dep = Dependator()
        >>> instance = dep.registerInstance('THE_INSTANCE')
        >>> instance.state
        0

        >>> dep.notifyPaused("THE_INSTANCE")
        True
        >>> instance.state
        4

        :type theInstName: str
        :param theInstName: Instance name to change state
        """
        return self._setState(theInstName, State.PAUSED)

    # =========================================================================
    def notifyDeleted(self, theInstName):
        """ Notify instance change to Deleted state

        >>> dep = Dependator()
        >>> instance = dep.registerInstance('THE_INSTANCE')
        >>> instance.state
        0

        >>> dep.notifyDeleted("THE_INSTANCE")
        True
        >>> instance.state
        5

        :type theInstName: str
        :param theInstName: Instance name to change state
        """
        return self._setState(theInstName, State.DELETED)

    # =========================================================================
    def notifyDestroyed(self, theInstName):
        """ Notify instance change to None state

        >>> dep = Dependator()
        >>> instance = dep.registerInstance('THE_INSTANCE')
        >>> instance.state
        0

        >>> dep.notifyDestroyed("THE_INSTANCE")
        True
        >>> instance.state
        0

        :type theInstName: str
        :param theInstName: Instance name to change state
        """
        return self._setState(theInstName, State.NONE)

    # =========================================================================
    def getInstanceState(self, theInstName):
        """ Get instance state

        >>> dep = Dependator()
        >>> instance = dep.registerInstance('THE_INSTANCE')
        >>> dep.notifyActived("THE_INSTANCE")
        True

        >>> dep.getInstanceState("NOT INSTANCE")

        >>> dep.getInstanceState("THE_INSTANCE")
        2

        :type theInstName: str
        :param theInstName: Instance name to get state
        """
        if theInstName in self.instances:
            return self.instances[theInstName].state
        else:
            None

    # =========================================================================
    def isNone(self, theInstName):
        """ Check if instance state is None

        >>> dep = Dependator()
        >>> instance = dep.registerInstance('THE_INSTANCE')

        >>> dep.isNone("NOT INSTANCE")
        False

        >>> dep.isNone("THE_INSTANCE")
        True

        >>> dep.notifyActived("THE_INSTANCE")
        True
        >>> dep.isNone("THE_INSTANCE")
        False

        :type theInstName: str
        :param theInstName: Instance name to get state

        :rtype: bool
        :return: True is instance stae is None else return False
        """
        return State.NONE == self.getInstanceState(theInstName)

    # =========================================================================
    def isCreated(self, theInstName):
        """ Check if instance state is Created

        >>> dep = Dependator()
        >>> instance = dep.registerInstance('THE_INSTANCE')

        >>> dep.isCreated("NOT INSTANCE")
        False

        >>> dep.isCreated("THE_INSTANCE")
        False

        >>> dep.notifyCreated("THE_INSTANCE")
        True
        >>> dep.isCreated("THE_INSTANCE")
        True

        :type theInstName: str
        :param theInstName: Instance name to get state

        :rtype: bool
        :return: True is instance stae is Created else return False
        """
        return State.CREATED == self.getInstanceState(theInstName)

    # =========================================================================
    def isActived(self, theInstName):
        """ Check if instance state is Actived

        >>> dep = Dependator()
        >>> instance = dep.registerInstance('THE_INSTANCE')

        >>> dep.isActived("NOT INSTANCE")
        False

        >>> dep.isActived("THE_INSTANCE")
        False

        >>> dep.notifyActived("THE_INSTANCE")
        True
        >>> dep.isActived("THE_INSTANCE")
        True

        :type theInstName: str
        :param theInstName: Instance name to get state

        :rtype: bool
        :return: True is instance stae is Active else return False
        """
        return State.ACTIVED == self.getInstanceState(theInstName)

    # =========================================================================
    def isWaiting(self, theInstName):
        """ Check if instance state is Waiting

        >>> dep = Dependator()
        >>> instance = dep.registerInstance('THE_INSTANCE')

        >>> dep.isWaiting("NOT INSTANCE")
        False

        >>> dep.isWaiting("THE_INSTANCE")
        False

        >>> dep.notifyWaiting("THE_INSTANCE")
        True
        >>> dep.isWaiting("THE_INSTANCE")
        True

        :type theInstName: str
        :param theInstName: Instance name to get state

        :rtype: bool
        :return: True is instance stae is Waiting else return False
        """
        return State.WAITING == self.getInstanceState(theInstName)

    # =========================================================================
    def isPaused(self, theInstName):
        """ Check if instance state is Paused

        >>> dep = Dependator()
        >>> instance = dep.registerInstance('THE_INSTANCE')

        >>> dep.isPaused("NOT INSTANCE")
        False

        >>> dep.isPaused("THE_INSTANCE")
        False

        >>> dep.notifyPaused("THE_INSTANCE")
        True
        >>> dep.isPaused("THE_INSTANCE")
        True

        :type theInstName: str
        :param theInstName: Instance name to get state

        :rtype: bool
        :return: True is instance stae is Paused else return False
        """
        return State.PAUSED == self.getInstanceState(theInstName)

    # =========================================================================
    def isDeleted(self, theInstName):
        """ Check if instance state is Deleted

        >>> dep = Dependator()
        >>> instance = dep.registerInstance('THE_INSTANCE')

        >>> dep.isDeleted("NOT INSTANCE")
        False

        >>> dep.isDeleted("THE_INSTANCE")
        False

        >>> dep.notifyDeleted("THE_INSTANCE")
        True
        >>> dep.isDeleted("THE_INSTANCE")
        True

        :type theInstName: str
        :param theInstName: Instance name to get state

        :rtype: bool
        :return: True is instance stae is Deleted else return False
        """
        return State.DELETED == self.getInstanceState(theInstName)

    # =========================================================================
    def setDependency(self, theInstName):
        """ Set a dependency for the given instace

        :type theInstName: str
        :param theInstName: Instance name to set dependency
        """
        pass

    # =========================================================================
    def getDependency(self, theInstName):
        """ Get dependency for the given instance

        :type theInstName: str
        :param theInstName: Instance name to get dependency
        """
        pass

    # =========================================================================
    def clearDependency(self, theInstName):
        """ Clear dependencyu for the given instance

        :type theInstName: str
        :param theInstName: Instance name to clear dependency
        """
        pass

    # =========================================================================
    def registerAttributeUpdate(self, theInstName, theAttrList):
        """ Register callback for the given attributes for the given instance

        :type theInstName: str
        :param theInstName: Instance name containing attributes to register

        :type theAttrList: tuple
        :param theAttrList: List of attributes to register for notification
        """
        pass

    # =========================================================================
    def deregisterAttributeUpdate(self):
        """
        """
        pass

    # =========================================================================
    def getRegisterAttributeUpdate(self):
        """
        """
        pass


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
