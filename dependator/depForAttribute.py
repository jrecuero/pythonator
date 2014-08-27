#!/usr/bin/env python

""" depForAttribute.py contains class DepForAttribute, which is the dependator
dependecy per attribute instance.

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
class DepForAttribute(object):
    """ Class were instance dependecies are stored
    """

    # =========================================================================
    def __init__(self,
                 theId,
                 theInstName,
                 theInstDep,
                 theAttrList,
                 theCallback,
                 thePriority=Priority.DEFAULT):
        """ Initializes a new dependency attribute

        >>> di = DepForAttribute(1, 'ME', 'YOU', ('a', 'b'), True)

        >>> di.id
        1

        >>> di.instName
        'ME'

        >>> di.instDep
        'YOU'

        >>> di.attrs
        ('a', 'b')

        >>> di.callback
        True

        >>> di.priority
        2

        :type theId: int
        :param theId: ID that identified the dependency

        :type theInstName: str
        :param theInstName: Instance name to set dependency

        :type theInstDep: str
        :param theInstDep: Instance name that contain attributes

        :type theAttrList: tuple
        :param theAttrList: List of attributes to depend

        :type theCallbacks: func
        :param theCallbacks: Notification to be called when attribute updated

        :type thePriority: Priority
        :param thePriority: Priority for callback notifications

        :rtype: int
        :return: ID for the new dependency entry created
        """
        self.id = theId
        """
        :type: int

        Dependency ID
        """

        self.instName  = theInstName
        """
        :type: str

        Dependency instance name that has dependecies
        """

        self.instDep   = theInstDep
        """
        :type: str

        Dependency instance name that has dependant attributes
        """

        self.attrs     = theAttrList
        """
        :type: list

        List with dependant attributes
        """

        self.callback = theCallback
        """
        :type: func

        Notification to be called when attributes are updated
        """

        self.priority  = thePriority
        """
        :type: Priority

        Dependency priority
        """

    # =========================================================================
    def __str__(self):
        """ Return string to be displayed when instance is printed

        >>> di = DepForAttribute(1, 'ME', 'YOU', ('a', 'b'), True)
        >>> print di
        1 : ME : YOU : ('a', 'b') : True : 2

        :rtype: str
        :return: String that represents the instance
        """
        return "%d : %s : %s : %s : %s : %s" %\
            (self.id, self.instName, self.instDep, self.attrs, self.callback, self.priority)


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
