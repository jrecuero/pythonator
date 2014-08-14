#!/usr/bin/env python

"""plist.py contains class PList, which is the basic implementation for
a priority list.

:author:    Jose Carlos Recuero
:version:   0.1
:since:     08/13/2014

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
# import user python modules
#
import loggerator
import error
import info


###############################################################################
##
##   ___ ___  _ __  ___| |_ __ _ _ __ | |_ ___
##  / __/ _ \| '_ \/ __| __/ _` | '_ \| __/ __|
## | (_| (_) | | | \__ \ || (_| | | | | |_\__ \
##  \___\___/|_| |_|___/\__\__,_|_| |_|\__|___/
##
###############################################################################
#

__trace__ = False

METHOD = 'method'
"""
    :type: str

    String that represents the key where the method for class
    PListFunction is being stored
"""

ARGS = 'args'
"""
    :type: str

    String that represents the key where list of arguments for class
    PListFunction is being stored
"""

KWARGS = 'kwargs'
"""
    :type: str

    String that represents the key where dictionary of arguments for class
    PListFunction is being stored
"""


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
class PriorityListException(error.BaseException):
    """Priority List Exception.
    Exception raised when a none valid list of priorities is passed. A valid
    list of priorities should never be None and it should be a list.

    >>> ex = PriorityListException()

    >>> ex.BASE_MESSAGE
    'Not valid priority list'

    >>> raise PriorityListException('custom plist exception')
    Traceback (most recent call last):
    ...
    PriorityListException: Not valid priority list : custom plist exception

    """
    BASE_MESSAGE = 'Not valid priority list'


#
# =============================================================================
#
class DefaultPriorityException(error.BaseException):
    """Default Priority Exception.
    Exception raised when the default value does not belont to the priority
    list.

    >>> ex = DefaultPriorityException()

    >>> ex.BASE_MESSAGE
    'Default priority not valid'

    >>> raise DefaultPriorityException('custom default priority')
    Traceback (most recent call last):
    ...
    DefaultPriorityException: Default priority not valid : custom default priority

    """
    BASE_MESSAGE = 'Default priority not valid'


#
# =============================================================================
#
class InvalidEntryException(error.BaseException):
    """Invalid Entry Exception.
    Exception raised when the entry to register to the priority list.
    is not valid. Entry validation depends on the priority list implementation
    but it should not be None at the least.

    >>> ex = InvalidEntryException()

    >>> ex.BASE_MESSAGE
    'Not a valid priority'

    >>> raise InvalidEntryException('custom invalid entry')
    Traceback (most recent call last):
    ...
    InvalidEntryException: Not a valid priority : custom invalid entry

    """
    BASE_MESSAGE = 'Not a valid priority'


#
# =============================================================================
#
class InvalidPriorityException(error.BaseException):
    """Invalid Priority Exception.
    Exception raised when the value does not belond to the list of priorities.

    >>> ex = InvalidPriorityException()

    >>> ex.BASE_MESSAGE
    'Priority is not in the priority list'

    >>> raise InvalidPriorityException('custom invalid priority')
    Traceback (most recent call last):
    ...
    InvalidPriorityException: Priority is not in the priority list : custom invalid priority

    """
    BASE_MESSAGE = 'Priority is not in the priority list'


#
# =============================================================================
#
class PValuesList(object):
    """PValuesList class stores information about a list of values handled as a
    list of priorities.

    This object is used to store a list of values which represent a list of
    priorities and a default value which will be the default priority.

    ::

        Data Structures:

            <priorities> as a list             <defaultPriority>
            ___________________________
            |    |    |    |     |    |
            | P1 | P2 | P3 | ... | Pn |         P1 <= Px <= Pn
            |____|____|____|_____|____|


    :type priorities: list
    :ivar priorities:
        List with all possible priorites in the class.

    :type defaultPriority: object
    :ivar defaultPriority:
        Value defines in priorities, and used by all method in PList as the
        default priority if no priority is provided.
    """

    # =========================================================================
    def __init__(self, priorities, defaultPriority, name=None):
        """PValuesList class constructor.

        >>> pl = PValuesList((1, 2, 3), 2, "custom enums")

        >>> pl.logger # doctest: +ELLIPSIS
        <loggerator.Loggerator object at 0x...>

        >>> pl.priorities
        (1, 2, 3)

        >>> pl.defaultPriority
        2

        >>> pl.name
        'custom enums'

        >>> pl = PValuesList((1, 2, 3), 2)

        >>> pl.name

        >>> pl = PValuesList((1, 2, 3), 0)
        Traceback (most recent call last):
        ...
        DefaultPriorityException: Default priority not valid : default: 0 not in (1, 2, 3)

        >>> pl = PValuesList(0, 0)
        Traceback (most recent call last):
        ...
        PriorityListException: Not valid priority list : priorities: 0

        :type priorities: list
        :param priorities:
            It is the list of priorities.

        :type defaultPriority: object
        :param defaultPriority:
            It is the default priority.

        :type name: str
        :param name: name for the list of priorities

        :raise PriorityListException:
            No list of priorities is provided.

        :raise DefaultPriorityException:
            Default priority does not belong to list of priorities provided.
        """
        if not priorities or isinstance(priorities, list):
            raise PriorityListException('priorities: %s' % (priorities, ))
        if not defaultPriority in priorities:
            raise DefaultPriorityException('default: %s not in %s' %
                                           (defaultPriority, priorities))

        self.logger          = loggerator.getLoggerator('pobject')
        self.priorities      = priorities
        self.defaultPriority = defaultPriority
        self.name            = name

    # =========================================================================
    def isValid(self, priority):
        """Check if the given priority is included in the list of priorities.

        It verifies that the given priority is valid and it is included in
        the list with all posssible priorities.

        :type priority: object
        :param priority:
            Priority to check if it is valid.

        :rtype: boolean
        :return:
            True if the priority is in the list of priorities. False if it is
            not found in the list of priorities.
        """
        return priority in self.priorities

    # =========================================================================
    def getList(self):
        """Return the list with all valid priorities.

        It returns a list with all possible valid priorities.

        :rtype: list
        :return:
            List with all priorities.
        """
        return self.priorities

    # =========================================================================
    def getDefault(self, priority=None):
        """Return the default priority value if the given priority is None.

        It returns the value for the default priority stored if the given
        priority is None.

        :type priority: object
        :param priority:
            Priority to use if valid.

        :raise InvalidPriorityException:
            Priority is not a valid one.
        """
        if priority is None:
            return self.defaultPriority
        else:
            if self.isValid(priority):
                return priority
        raise InvalidPriorityException('priority: %s' % priority)


#
###############################################################################
#
class PList(object):
    """PList class provides a base class for a priority list.

    It wrappers up a class, where items are organized in physically different
    list per priority.

    A PList is mainly a list of lists. The first/top list is kept in attribute
    'container', which is a list where the index identify the priority.
    The list of priorities, together with the default priority is stored in a
    PValuesList instance.

    For every entry in the container, one per priority, we have a list of
    entries, which could be any kind of object.

    ::

        <priorityValues> as PValuesList instance.
        _________________
        |           |    |
        | P1 .. Pn  | Px |
        |___________|____|

        <container> as a list
        _______                    _______________________________
        |     |                    |       |       |     |       |
        | P1  | ---> container[P1] | Data1 | Data2 | ... | DataN |
        |_____|                    |_______|_______|_____|_______|
        |     |
        | P2  |
        |_____|
        |     |
        | P3  |
        |_____|
        |     |
        | ... |
        |_____|                    _______________________________
        |     |                    |       |       |     |       |
        | Pn  | ---> container[Pn] | Data1 | Data2 | ... | DataN |
        |_____|                    |_______|_______|_____|_______|

    Data entries (Data1, ..., DataN) can be added at the Front (before Data1)
    or at the Back (after DataN) for every container[Pn].

    :type priorityValues: PValuesList
    :ivar priorityValues:
        PValuesList with the list with all possible priorites and the default
        one.

    :type container: dict
    :ivar container:
        Dictionary, where every key is a value in priorities, and which
        value is the list of object for such priority.
    """

    # =========================================================================
    def __init__(self, priorities, defaultPriority, name=None):
        """PList class constructor.

        Create a PList instance with a the given list of priorities, and where
        the default priority when an entry is added is de default value
        provided in the constructor.

        A list will be created per entry in the list of priorities.

        :type priorities: list
        :param priorities:
            It is the list of priorities to be used in the priority list.

        :type defaultPriority: object
        :param defaultPriority:
            It is the default priority that will be used for any other method
            when no priority value is provided.
            This value should be present in the list of priorities provided in
            this constructor.

        :type name: str
        :param name: name for the list

        :raise PriorityListException:
            No list of priorities is provided.

        :raise DefaultPriorityException:
            Default priority does not belong to list of priorities provided.
        """
        if not priorities or isinstance(priorities, list):
            raise PriorityListException()

        if not defaultPriority in priorities:
            raise DefaultPriorityException()

        self.logger         = loggerator.getLoggerator('plist')
        self.priorityValues = PValuesList(priorities, defaultPriority)
        self.name           = name
        self.container      = {}
        for priority in self.priorityValues.getList():
            self.container[priority] = []

    # =========================================================================
    def _validateEntry(self, entry):
        """Validate entry before inserting it.

        It validates entry is valid for the priority list. This method should
        be overriden by any specialized derived class.

        :type entry: object
        :param entry:
            Object to be validated before being inserted.

        :raise InvalidEntryException:
            Entry is None or not valid.
        """
        if entry is None:
            raise InvalidEntryException('Entry: %s' % entry)

    # =========================================================================
    def _getEntryFromContainer(self, entry, priority):
        """Get entry from the container.

        This method returns the entry from the container for the given priority
        that is related with the given entry parameter.

        It can be overriden in derived classes in order to provide the
        real entry to be used, because the entry parameter could not be
        the same as the entry in the container for derived classes.

        :type entry: object
        :param entry:
            Object to be check is present in the container.

        :type priority: int
        :param priority:
            Priority of the container where entry should be checked if present.

        :rtype: object
        :return:
            Entry to be removed or None if not found.
        """
        return entry if entry in self.container[priority] else None

    # =========================================================================
    def addAtFront(self, entry, priority=None):
        """Add a new entry at the top/front of the list for the given priority.

        It adds the given entry in the list for the given priority, and it
        adds at the start/front of the list.

        :type entry: object
        :param entry:
            Object to be added at the front of the list.

        :type priority: object
        :param priority:
            Priority where the object should be added. If no value is
            provided, default priority will be used.

        :rtype: object
        :return:
            Object added if it was inserted properly.

        :raise InvalidEntryException:
            Entry is None or not valid.

        :raise InvalidPriorityException:
            Priority is not a valid one.
        """
        self._validateEntry(entry)
        priority = self.priorityValues.getDefault(priority)
        self.container[priority].insert(0, entry)
        if __debug__:
            self.logger.debug('%s entry %s added front priority list %s' %
                              (info.FUNC(), entry, priority))
        return entry

    # =========================================================================
    def addAtBack(self, entry, priority=None):
        """Add a new entry at the back/end of the list for the given priority.

        It adds the given entry in the list for the given priority , and it
        adds at the back/end of the list.

        :type entry: object
        :param entry:
            Object to be added at the back of the list.

        :type priority: object
        :param priority:
            Priority where the object should be added. If no value is
            provided, default priority will be used.

        :rtype: object
        :return:
            Object added if it was inserted properly.

        :raise InvalidEntryException:
            Entry is None or not valid.

        :raise InvalidPriorityException:
            Priority is not a valid one.
        """
        self._validateEntry(entry)
        priority = self.priorityValues.getDefault(priority)
        self.container[priority].append(entry)
        if __debug__:
            self.logger.debug('%s entry %s added back priority list %s' %
                              (info.FUNC(), entry, priority))
        return entry

    # =========================================================================
    def addAtFrontForAll(self, entry):
        """Add a new entry at the front for every priority.

        It adds the given entry for every priority, and it adds at the front
        for every list

        :type entry: object
        :param entry:
            Object to be added at the front of the list.

        :rtype: list
        :return:
            List with all objects added if they were inserted properly.

        :raise InvalidEntryException:
            Entry is None or not valid.
        """
        self._validateEntry(entry)
        if __debug__:
            self.logger.debug('%s entry %s added front' %
                              (info.FUNC(), entry))
        return map(lambda x:
                   self.addAtFront(entry, x), self.priorityValues.getList())

    # =========================================================================
    def addAtBackForAll(self, entry):
        """Add a new entry at the back for every priority.

        It adds the given entry for every priority, and it adds at the back for
        every list

        :type entry: object
        :param entry:
            Object to be added at the back of the list.

        :rtype: list
        :return:
            List with all objects added if they were inserted properly.

        :raise InvalidEntryException:
            Entry is None or not valid.
        """
        if __debug__:
            self.logger.debug('%s entry %s added back' %
                              (info.FUNC(), entry))
        self._validateEntry(entry)
        return map(lambda p:
                   self.addAtBack(entry, p), self.priorityValues.getList())

    # =========================================================================
    def remove(self, entry, priority=None):
        """Remove the given entry from the given priority list.

        It removes the given entry from the list for the given priority.

        :type entry: object
        :param entry:
            Object to be removed from the list.

        :type priority: object
        :param priority:
            Priority where the object should be removed. If no value is
            provided, default priority will be used.

        :rtype: object
        :return:
            Object removed if it was found. None if object was not found.

        :raise InvalidEntryException:
            Entry is None or not valid.

        :raise InvalidPriorityException:
            Priority is not a valid one.
        """
        self._validateEntry(entry)
        priority = self.priorityValues.getDefault(priority)
        if __debug__:
            self.logger.debug('%s entry %s removed priority list %s' %
                              (info.FUNC(), entry, priority))
        retvalue = None
        realEntry = self._getEntryFromContainer(entry, priority)
        if realEntry is not None:
            self.container[priority].remove(realEntry)
            retvalue = self._getValueFromEntry(realEntry)
            if __debug__:
                self.logger.debug('%s real entry %s removed priority list %s' %
                                  (info.FUNC(), retvalue, priority))
        return retvalue

    # =========================================================================
    def removeForAll(self, entry):
        """Remove the given entry from all priorities.

        It removes the given entry from every priority list.

        :type entry: object
        :param entry:
            Object to be removed from the list.

        :rtype: list
        :return:
            List with all objects removed if they were found. If the object
            was not found for any priority, it returns a None for such
            priority.

        :raise InvalidEntryException:
            Entry is None or not valid.
        """
        if __debug__:
            self.logger.debug('%s entry %s removed' %
                              (info.FUNC(), entry))
        self._validateEntry(entry)
        return map(lambda p:
                   self.remove(entry, p), self.priorityValues.getList())

    # =========================================================================
    def getListForPriority(self, priority=None):
        """Return the list for the given priority.

        It returns the list with all entries for the given priority.

        :type priority: object
        :param priority:
            Priority of the list to be returned, If no value is given for the
            priority, the default priority will be used.

        :rtype: list
        :return:
            List with all entries for the given priority.

        :raise InvalidPriorityException:
            Priority is not a valid one.
        """
        priority = self.priorityValues.getDefault(priority)
        return self.container[priority]

    # =========================================================================
    def getAllLists(self):
        """Return all lists.

        It returns all list for every priority. List is concatenated in the
        order of the priority, first the one with highest priority and so on.

        The list returned doesn't have any information about which entries
        belong to whar priority.

        :rtype: list
        :return:
            All priority list concatenaited.
        """
        retvalue = []
        for priority in self.priorityValues.getList():
            retvalue += self.container[priority]
        return retvalue

    # =========================================================================
    def cleanList(self, priority=None):
        """Clean a list for the given priority.

        It cleans a list for the given priority, removing all entries for
        that list.

        :type priority: object
        :param priority:
            Priority of the list to be cleaned, If no value is given for the
            priority, the default priority will be used.

        :raise InvalidPriorityException:
            Priority is not a valid one.
        """
        priority = self.priorityValues.getDefault(priority)
        del self.container[priority][:]

    # =========================================================================
    def cleanListForAll(self):
        """Clean all lists.

        It cleans all priority lists.
        """
        for priority in self.priorityValues.getList():
            self.cleanList(priority)

    # =========================================================================
    def lenInList(self, priority=None):
        """Number of entries in the list for the given priority.

        It returns the length for the list for the given priority.

        :type priority: object
        :param priority:
            Priority of the list which length is requested, If no value is
            given for the priority, the default priority will be used.

        :rtype: int
        :return:
            Length for the given priority

        :raise InvalidPriorityException:
            Priority is not a valid one.
        """
        priority = self.priorityValues.getDefault(priority)
        return len(self.container[priority])


#
#############################################################################
#
class PListFunction(PList):
    """PListFunction extend PList where elements stored are functions.

    It is a PList extension where values entered in the priority list are
    method calls.

    Every entry should be a dictionary with three keys:

    +--------+---------------------------+
    | key    | value                     |
    +========+===========================+
    | method | method call               |
    +--------+---------------------------+
    | args   | args to pass to method    |
    +--------+---------------------------+
    | kwargs | kwargs to pass to method  |
    +--------+---------------------------+

    ::

                            ____________________________________________________
        <container[Pn]> --> |                                                  |
                            | <Entry> as a dictionary                          |
                            |                                                  |
                            | Entry['method'] -> method call                   |
                            | Entry['args']   -> args to pass to method call   |
                            | Entry['kwargs'] -> kwargs to pass to method call |
                            |__________________________________________________|

    """

    # =========================================================================
    def _validateEntry(self, entry):
        """Validate method is valid.

        It validate the method provided is a function call.

        :type entry: object
        :param entry:
            Method to be validated before being inserted.

        :raise InvalidEntryException:
            Entry is None or not valid.
        """
        if entry is not None and METHOD in entry and hasattr(entry[METHOD], '__call__'):
            if not ARGS in entry:
                entry[ARGS] = ()
            if not KWARGS in entry:
                entry[KWARGS] = {}
        else:
            raise InvalidEntryException('Entry: %s' % entry)

    # =========================================================================
    def _getEntryFromContainer(self, method, priority):
        """Get entry from the container.

        This method returns the entry from the container for the given priority
        that is related with the given method parameter.

        In this case the parameter method is the method stored in the priority
        list with key equal to 'method', and the value returned should be the
        real entry in the container for the given priority.

        :type method: function
        :param method:
            Method to be check is present in the container.

        :type priority: int
        :param priority:
            Priority of the container where entry should be checked if present.

        :rtype: object
        :return:
            Real entry in the container to be removed or None if not found.
        """
        for traverse in self.container[priority]:
            if method[METHOD] == traverse[METHOD]:
                return traverse
        return None

    # =========================================================================
    def _getValueFromEntry(self, entry):
        """ Return value to return when an entry is found.

        This method is used to return the method inside any entry stored in the
        PListFunction.

        :type entry: dict
        :param entry: Entry found in the PListFunction.

        :rtype: function
        :return: Function stored in the entry in the PListFunction.
        """
        return entry['method']

    # =========================================================================
    def _callEntry(self, entry, *args, **kwargs):
        """Call method in the given entry.

        It get the method, args and kwargs from the given entry, and proceed
        to call it.

        :type entry: dict
        :param entry:
            Dictionary containing method, args and kwargs.
        """
        method = entry[METHOD]
        argsToUse = list(entry[ARGS])
        argsToUse.extend(args)
        kwargsToUse = entry[KWARGS]
        kwargsToUse.update(kwargs)
        if __trace__:
            self.logger.debug('%s method %s, args %s, kwargs %s' %
                              (info.FUNC(), method, argsToUse, kwargsToUse))
        method(*argsToUse, **kwargsToUse)

    # =========================================================================
    def callForPriority(self, priority=None, *args, **kwargs):
        """Call all methods for the given priority.

        It calls all methods for the given priority.

        :type priority: object
        :param priority:
            Priority of the list where methods should be called, If no value is
            given for the priority, the default priority will be used.

        :raise InvalidPriorityException:
            Priority is not a valid one.
        """
        priority = self.priorityValues.getDefault(priority)
        if __trace__:
            self.logger.debug('%s priority %s, args %s, kwargs %s' %
                              (info.FUNC(), priority, args, kwargs))
        for entry in self.container[priority]:
            self._callEntry(entry, *args, **kwargs)

    # =========================================================================
    def callForAll(self, *args, **kwargs):
        """Call all methods.

        It calls all methods for every priority.
        """
        if __trace__:
            self.logger.debug('%s args %s, kwargs %s' %
                              (info.FUNC(), args, kwargs))
        for priority in self.priorityValues.getList():
            self.callForPriority(priority, *args, **kwargs)

    # =========================================================================
    def remove(self, entry, priority=None):
        """Remove the given entry from the given priority list.

        It removes the given entry from the list for the given priority.

        :type entry: object
        :param entry:
            Object to be removed from the list.

        :type priority: object
        :param priority:
            Priority where the object should be removed. If no value is
            provided, default priority will be used.

        :rtype: object
        :return:
            Object removed if it was found. None if object was not found.

        :raise InvalidEntryException:
            Entry is None or not valid.

        :raise InvalidPriorityException:
            Priority is not a valid one.
        """
        self._validateEntry(entry)
        priority = self.priorityValues.getDefault(priority)
        if __debug__:
            self.logger.debug('%s entry %s removed priority list %s' %
                              (info.FUNC(), entry, priority))
        retvalue = None
        realEntry = self._getEntryFromContainer(entry, priority)
        if realEntry is not None:
            self.container[priority].remove(realEntry)
            retvalue = realEntry[METHOD]
            if __debug__:
                self.logger.debug('%s real entry %s removed priority list %s' %
                                  (info.FUNC(), realEntry[METHOD], priority))
        return retvalue


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
