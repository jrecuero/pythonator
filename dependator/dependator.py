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
#from dependator.state import State
#from dependator.priority import Priority
#from dependator.depForInstance import DepForInstance
#from dependator.depForAttribute import DepForAttribute


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
        """
        """
        pass

    # =========================================================================
    def registerInstance(self, theInstNamej):
        """ Register instance to dependator

        :type theInstNamej: str
        :param theInstNamej: Instance name to register
        """
        pass

    # =========================================================================
    def deregisterInstance(self, instNamej):
        """ Deregister instance from the dependator

        :type theInstNamej: str
        :param theInstNamej: Instance name to deregister
        """
        pass

    # =========================================================================
    def setDependency(self, instNamej):
        """ Set a dependency for the given instace

        :type theInstNamej: str
        :param theInstNamej: Instance name to set dependency
        """
        pass

    # =========================================================================
    def getDependency(self, theInstNamej):
        """ Get dependency for the given instance

        :type theInstNamej: str
        :param theInstNamej: Instance name to get dependency
        """
        pass

    # =========================================================================
    def clearDependency(self, theInstNamej):
        """ Clear dependencyu for the given instance

        :type theInstNamej: str
        :param theInstNamej: Instance name to clear dependency
        """
        pass

    # =========================================================================
    def registerAttributeUpdate(self, theInstNamej, theAttrList):
        """ Register callback for the given attributes for the given instance

        :type theInstNamej: str
        :param theInstNamej: Instance name containing attributes to register

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

    # =========================================================================
    def notifyCreated(self, theInstNamej):
        """ Notify instance change to Created state

        :type theInstNamej: str
        :param theInstNamej: Instance name to change state
        """
        pass

    # =========================================================================
    def notifyActived(self, theInstNamej):
        """ Notify instance change to Actived state

        :type theInstNamej: str
        :param theInstNamej: Instance name to change state
        """
        pass

    # =========================================================================
    def notifyWaiting(self, theInstNamej):
        """ Notify instance change to Waiting state

        :type theInstNamej: str
        :param theInstNamej: Instance name to change state
        """
        pass

    # =========================================================================
    def notifyPaused(self, theInstNamej):
        """ Notify instance change to Paused state

        :type theInstNamej: str
        :param theInstNamej: Instance name to change state
        """
        pass

    # =========================================================================
    def notifyDeleted(self, theInstNamej):
        """ Notify instance change to Deleted state

        :type theInstNamej: str
        :param theInstNamej: Instance name to change state
        """
        pass

    # =========================================================================
    def notifyDestroyed(self, theInstNamej):
        """ Notify instance change to None state

        :type theInstNamej: str
        :param theInstNamej: Instance name to change state
        """
        pass

    # =========================================================================
    def getInstanceState(self, theInstNamej):
        """ Get instance state

        :type theInstNamej: str
        :param theInstNamej: Instance name to get state
        """
        pass

    # =========================================================================
    def isNone(self, theInstNamej):
        """ Check if instance state is None

        :type theInstNamej: str
        :param theInstNamej: Instance name to get state

        :rtype: bool
        :return: True is instance stae is None else return False
        """
        pass

    # =========================================================================
    def isCreated(self, theInstNamej):
        """ Check if instance state is Created

        :type theInstNamej: str
        :param theInstNamej: Instance name to get state

        :rtype: bool
        :return: True is instance stae is Created else return False
        """
        pass

    # =========================================================================
    def isActived(self, theInstNamej):
        """ Check if instance state is Actived

        :type theInstNamej: str
        :param theInstNamej: Instance name to get state

        :rtype: bool
        :return: True is instance stae is Active else return False
        """
        pass

    # =========================================================================
    def isWaiting(self, theInstNamej):
        """ Check if instance state is Waiting

        :type theInstNamej: str
        :param theInstNamej: Instance name to get state

        :rtype: bool
        :return: True is instance stae is Waiting else return False
        """
        pass

    # =========================================================================
    def isPaused(self, theInstNamej):
        """ Check if instance state is Paused

        :type theInstNamej: str
        :param theInstNamej: Instance name to get state

        :rtype: bool
        :return: True is instance stae is Paused else return False
        """
        pass

    # =========================================================================
    def isDeleted(self, theInstNamej):
        """ Check if instance state is Deleted

        :type theInstNamej: str
        :param theInstNamej: Instance name to get state

        :rtype: bool
        :return: True is instance stae is Deleted else return False
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
