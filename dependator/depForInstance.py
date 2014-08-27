#!/usr/bin/env python

""" depForInstace.py contains class DepForInstance, which is the dependator
dependecy per instance.

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
class DepForInstance(object):
    """ Class were instance dependecies are stored
    """

    # =========================================================================
    def __init__(self,
                 theId,
                 theInstName,
                 theDeps,
                 theCallbacks,
                 thePriority=Priority.DEFAULT):
        """ Initializes a new dependency instance

        >>> di = DepForInstance(1, 'ME', ('YOU', 'HIM'), {'actived': True})

        >>> di.id
        1

        >>> di.instName
        'ME'

        >>> di.deps
        ['HIM', 'YOU']

        >>> di.callbacks
        {'actived': True}

        >>> di.priority
        2

        :type theId: int
        :param theId: ID that identified the dependency

        :type theInstName: str
        :param theInstName: Instance name to set dependency

        :type theDeps: tuple
        :param theDeps: List with all dependencies

        :type theCallbacks: dict
        :param theCallbacks: Dictionary with callbacks for every notification

        :type thePriority: Priority
        :param thePriority: Priority for callback notifications

        :rtype: int
        :return: ID for the new dependency entry created
        """

        self.id        = theId
        """
        :type: int

        Dependency ID
        """

        self.instName  = theInstName
        """
        :type: str

        Dependency instance name that has dependecies
        """

        self.deps = list(theDeps)
        self.deps.sort()
        """
        :type: list

        List of dependencies (sorted)
        """

        self.callbacks = theCallbacks
        """
        :type: dict

        Dictionary with notification for dependencies
        """

        self.priority  = thePriority
        """
        :type: Priority

        Dependency priority
        """

    # =========================================================================
    def __str__(self):
        """ Return string to be displayed when instance is printed

        >>> di = DepForInstance(1, 'ME', ('YOU', 'HIM'), {'actived': True})
        >>> print di
        1 : ME : ['HIM', 'YOU'] : {'actived': True} : 2

        :rtype: str
        :return: String that represents the instance
        """
        return "%d : %s : %s : %s : %s" %\
            (self.id, self.instName, self.deps, self.callbacks, self.priority)

    # =========================================================================
    def match(self, theInstName, theDeps):
        """ Match same instance and dependecies with given values

        >>> di = DepForInstance(1, 'ME', ('YOU', 'HIM'), {'actived': True})

        >>> di.match('ME', ('YOU', 'HIM'))
        True

        >>> di.match('YOU', ('YOU', 'HIM'))
        False

        >>> di.match('ME', ('YOU', ))
        False

        :type theInstName: str
        :param theInstName: Instance name to match

        :type theDeps: tuple
        :param theDeps: List with all dependencies to match

        :rtype: bool
        :return: True if the same instance and dependencies else False
        """

        lista = list(theDeps)
        lista.sort()
        return self.instName == theInstName and self.deps == lista


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
