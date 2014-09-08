#!/usr/bin/env python

""" notificator.py contains class Notificator, which is the
the base implementation for a notification manager using
priority lists.

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
import functools
import mock

#
# import user python modules
#
import plist
import info
import error
import loggerator


###############################################################################
##
##   ___ ___  _ __  ___| |_ __ _ _ __ | |_ ___
##  / __/ _ \| '_ \/ __| __/ _` | '_ \| __/ __|
## | (_| (_) | | | \__ \ || (_| | | | | |_\__ \
##  \___\___/|_| |_|___/\__\__,_|_| |_|\__|___/
##
###############################################################################
#
ID = 'id'
"""
    :type: str

    String that represents the key for the Id for the value returned when a
    trigger method is registered to the Notificator.
"""

TRIGGER = 'trigger'
"""
    :type: str

    String that represents the key for the trigger method for the value
    returned when a trigger method is registerd to the NotifyManager.
    String that represents the key for the trigger method for the dictionary
    where information about all triggers
    methods are stored.
"""

METHOD = 'method'
"""
    :type: str

    String that represents the key for the notification method for the
    dictionary where informaton about all notification methods are stored.
    Notification are callback registered to trigger methods.
"""

ARGS = 'args'
"""
    :type: str

    String that represents the key for the list of arguments passed to the
    trigger method for the dictionary where information about all triggers
    methods are stored.
    String that represents the key for the list of arguments passed to the
    notification method for the dictionary where informaton about all
    notification methods are stored.
    Notification are callback registered to trigger methods.
"""

KWARGS = 'kwargs'
"""
    :type: str

    String that represents the key for the dictionary of arguments passed to
    the trigger method for the dictionary where information about all triggers
    methods are stored.
    String that represents the key for the dictionary of arguments passed to
    the notification method for the dictionary where informaton about all
    notification methods are stored.
    Notification are callback registered to trigger methods.
"""

PLIST   = 'plist'
"""
    :type: str

    String that represents the key where priority list instance for
    notifications registered to trigger methods are stored.
"""

BEFORE  = 'before'
"""
    :type: str

    String that represents the key where where notifications registered to be
    called before the trigger method runs are stored.
"""

AFTER   = 'after'
"""
    :type: str

    String that represents the key where where notifications registered to be
    called after the trigger method runs are stored.
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
class InvalidIdException(error.BaseException):
    """Invalid Id Exception.
    Exception raised when an invalid id is passed to the notification manager.
    A valid id should be in the range of ids with trigger methods registered
    to the notification manager.

    >>> ex = InvalidIdException()

    >>> ex.BASE_MESSAGE
    'Invalid ID provided'

    >>> raise InvalidIdException('custom invalid id')
    Traceback (most recent call last):
    ...
    InvalidIdException: Invalid ID provided : custom invalid id

    """
    BASE_MESSAGE = "Invalid ID provided"


#
# =============================================================================
#
class InvalidMethodCallException(error.BaseException):
    """Invalid Method Call Exception.
    Exception raised when an invalid method call is passed to the notification
    manager. A valid method call should have a '__call__' attribute in order to
    be able to call it.

    >>> ex = InvalidMethodCallException()

    >>> ex.BASE_MESSAGE
    'Invalid method call provided'

    >>> raise InvalidMethodCallException('custom invalid method')
    Traceback (most recent call last):
    ...
    InvalidMethodCallException: Invalid method call provided : custom invalid method

    """
    BASE_MESSAGE = "Invalid method call provided"


#
# =============================================================================
#
class RegistrationException(error.BaseException):
    """Registration Exception.
    Exception raised when a registration for a trigger method or a notification
    method fail.

    >>> ex = RegistrationException()

    >>> ex.BASE_MESSAGE
    'Registration failed'

    >>> raise RegistrationException('custom registration failed')
    Traceback (most recent call last):
    ...
    RegistrationException: Registration failed : custom registration failed

    """
    BASE_MESSAGE = "Registration failed"


#
# =============================================================================
#
class DeregistrationException(error.BaseException):
    """Deregistration Exception.
    Exception raised when a deregistration for a trigger method or a
    notification method fail.

    >>> ex = DeregistrationException()

    >>> ex.BASE_MESSAGE
    'Deregistration failed'

    >>> raise DeregistrationException('custom deregistration failed')
    Traceback (most recent call last):
    ...
    DeregistrationException: Deregistration failed : custom deregistration failed

    """
    BASE_MESSAGE = "Deregistration failed"


#
# =============================================================================
#
class TriggerException(error.BaseException):
    """Trigger Exception.
    Exception raised when a trigger method failed in its execution.

    >>> ex = TriggerException()

    >>> ex.BASE_MESSAGE
    'Trigger failed'

    >>> raise TriggerException('custom Trigger failed')
    Traceback (most recent call last):
    ...
    TriggerException: Trigger failed : custom Trigger failed

    """
    BASE_MESSAGE = "Trigger failed"


#
# =============================================================================
#
class Notificator(object):
    """Notificator provides notifications for clients subscribed.

    Notificator implements a notification manager which provides priority
    notifications to be called at the front or at the back of a registered
    event.

    The way in which it works is this:

        - Notificator provides a registration mechanism, which clients will
          use to register trigger methods. That registration will return a new
          method that replaces the trigger method and a handler/id which will
          be used to register notification to that trigger.

        - Client can use that handler to register notifications to be called
          before the trigger method is executed, or after the trigger method
          has been executed.

        - Those notification can be use different priorities.

        - When the trigger method is called, the handler/id will be used in
          order to properly retrieve all notification to be called at any
          stage (before or after).

    ::

        Data Structures:

            <priorityValues> as PValuesList instance.
            _________________
            |           |    |
            | P1 .. Pn  | Px |
            |___________|____|


            <triggerInfo> as a dictionary
            ___________________
            |         |       |
            | Key: ID | Value |
            |_________|_______|


            <triggerInfo[ID]> as a dictionary
            ____________________________________________________________
            |               |                                          |
            | Key: 'method' | trigger method                           |
            |_______________|__________________________________________|
            |               |                                          |
            | Key: 'args'   | args to pass to trigger                  |
            |_______________|__________________________________________|
            |               |                                          |
            | Key: 'kwargs' | kwargs to pass to trigger                |
            |_______________|__________________________________________|
            |               |                                          |
            | Key: 'plist'  | Dictionary with PList for notifications  |
            |_______________|__________________________________________|


            <trigger.Value['plist']> as a dictionary
            _______________________________________________________________________
            |               |                                                     |
            | Key: 'before' | PList with notification to be called before trigger |
            |_______________|_____________________________________________________|
            |               |                                                     |
            | Key: 'after'  | PList with notification to be called after trigger  |
            |_______________|_____________________________________________________|



    """

    # =========================================================================
    def __init__(self, priorities, defaultPriority):
        """Notificator constructor.

        It create a Notificator instance. Initialize Id to zero.

        >>> nt = Notificator((1, 2, 3), 2)

        >>> nt.logger # doctest: +ELLIPSIS
        <loggerator.Loggerator object at 0x...>

        >>> nt.priorityValues # doctest: +ELLIPSIS
        <plist.PValuesList object at 0x...>

        >>> nt.id
        0

        >>> nt.triggerInfo
        {}

        :type priorities: list
        :param priorities:
            It is the list of priorities to be used in the priority list.

        :type defaultPriority: object
        :param defaultPriority:
            It is the default priority that will be used for any other method
            when no priority value is provided.

        :raise plist.PriorityListException:
            No list of priorities is provided.

        :raise plist.DefaultPriorityException:
            Default priority does not belong to the list of priorities provided.
        """
        self.logger = loggerator.getLoggerator('notificator',
                                               color=(loggerator.FG_YELLOW))
        """
            :type: loggerator.Loggerator

            Variable for local logger. Disable debug logs by default.
        """

        self.priorityValues = plist.PValuesList(priorities, defaultPriority)
        """
            :type: PValuesList

            PValuesList with the list with all possible priorites and the
            default one.
        """

        self.id          = 0
        """
            :type: int

            Identification for every function registered to the notify manager.
        """

        self.triggerInfo = {}
        """
            :type: dict

            Dictionary where triggers functions will be stored. A trigger
            function is the trigger provided by the user wrapped up in order
            to call all notification registered to that trigger.

            **triggerInfo** dictionary

            +----------+-----------+----------------------+------------+
            | Key      | KeyType   | Value                | Value Type |
            +==========+===========+======================+============+
            | ID       |  <int>    | Trigger Info         | <dict>     |
            +----------+-----------+----------------------+------------+

            **triggerInfo[ID]** dictionary

            +----------+---------+----------------------+------------+
            | Key      | KeyType | Value                | Value Type |
            +==========+=========+======================+============+
            +----------+---------+----------------------+------------+
            | 'method' |  <str>  | Trigger method       | <func>     |
            +----------+-----------+--------------------+------------+
            | 'args'   | <str>   | Trigger(args)        | <list>     |
            +----------+-----------+--------------------+------------+
            | 'kwargs' | <str>   | Trigger(kwargs)      | <dict>     |
            +----------+-----------+--------------------+------------+
            | 'plist'  | <str>   | Notifications        | <dict>     |
            +----------+-----------+--------------------+------------+

            **triggerInfo[ID]['plist']** dictionary

            +----------+-----------+--------------------+------------+
            | Key      | KeyType | Value                | Value Type |
            +==========+=========+======================+============+
            | 'before' | <str>   | Before notifications | <PList>    |
            +----------+-----------+--------------------+------------+
            | 'after'  | <str>   | After notifications  | <PList>    |
            +----------+---------+----------------------+------------+
        """

    # =========================================================================
    def _increaseId(self):
        """Increase the notify manager instance id and return
        the new value.

        >>> nt = Notificator((1, 2, 3), 2)

        >>> nt._increaseId()
        1
        >>> nt.id
        1

        >>> nt._increaseId()
        2
        >>> nt.id
        2

        :rtype: int
        :return:
            New value for the instance id.
        """
        self.id += 1
        return self.id

    # =========================================================================
    def _isValidId(self, id):
        """Check if the given id is a valid one.

        It checks if the given id value is a valid one, and it will be a valid
        one if it is a valid/active key. It has to be lower or equal that the
        actual key value.

        >>> nt = Notificator((1, 2, 3), 2)
        >>> nt.id = 2
        >>> nt.triggerInfo = {1: True, 2: True, }

        >>> nt._isValidId(1)
        True

        >>> nt._isValidId(2)
        True

        >>> nt._isValidId(3)
        False

        :type id: int
        :param id:
            Id to check if it is valid.

        :rtype: boolean
        :return:
            True if the given id is valid. False if the given id is not valid.
        """
        return id <= self.id and id in self.triggerInfo.keys()

    # =========================================================================
    def _validateId(self, id):
        """Validate the given id.

        If the given id is not validated, it raises an exception.

        >>> nt = Notificator((1, 2, 3), 2)
        >>> nt.id = 2
        >>> nt.triggerInfo = {1: True, 2: True, }

        >>> nt._validateId(1)

        >>> nt._validateId(2)

        >>> nt._validateId(3)
        Traceback (most recent call last):
        ...
        InvalidIdException: Invalid ID provided : id: 3

        :type id: int
        :param id:
            Id to check if it is valid.

        :raise InvalidIdException:
            Id give is not a valid one.
        """
        if not self._isValidId(id):
            raise InvalidIdException('id: %s' % id)

    # =========================================================================
    def _isMethodType(self, method):
        """Check if the given method is a valid one.

        It checks if the given method object is valid. It will valid if
        it is not None and it is a method call.

        >>> nt = Notificator((1, 2, 3), 2)

        >>> def say():
        ...     pass
        >>> nt._isMethodType(say)
        True

        >>> value = 0
        >>> nt._isMethodType(value)
        False

        >>> value = 1
        >>> nt._isMethodType(value)
        False

        >>> lista = []
        >>> nt._isMethodType(lista)
        False

        :type method: function
        :param method:
            Notification object to check if it is valid.

        :rtype: boolean
        :return:
            True if the given method is valid. False if the given
            method is not valid.
        """
        if method and hasattr(method, '__call__'):
            return True
        return False

    # =========================================================================
    def _validateMethodCall(self, method):
        """Validate the given method call.

        If the given method calls is not a valid one, it raises an exception.

        >>> nt = Notificator((1, 2, 3), 2)

        >>> def say():
        ...     pass
        >>> nt._validateMethodCall(say)

        >>> value = 0
        >>> nt._validateMethodCall(value)
        Traceback (most recent call last):
        ...
        InvalidMethodCallException: Invalid method call provided : method call: 0

        :type method: function
        :param method:
            Notification object to check if it is valid.

        :raise InvalidMethodCallException:
            Method call is not a valid one.
        """
        if not self._isMethodType(method):
            raise InvalidMethodCallException('method call: %s' % method)
        # This is required for testing with Mock functions, because they are
        # required to have a __name__ attribute in order to work with
        # @functools.wraps decorator or any toher feature that requires the
        # proper __name__ function attribute to be set.
        if isinstance(method, mock.Mock):
            method.__name__ = method._mock_name

    # =========================================================================
    def _validatePriorityValue(self, priority):
        """Validate the given priority value.

        If the given priority value is not a valid one, it raises an exception.

        >>> nt = Notificator((1, 2, 3), 2)

        >>> nt._validatePriorityValue(1)

        >>> nt._validatePriorityValue(0)
        Traceback (most recent call last):
        ...
        InvalidPriorityException: Priority is not in the priority list : priority: 0 not in (1, 2, 3)


        :type priority: object
        :param priority:
            Notification object to check if it is valid.

        :raise plist.InvalidPriorityException:
            Priority value is not a valid one.
        """
        if not self.priorityValues.isValid(priority):
            raise plist.InvalidPriorityException('priority: %s not in %s' %
                                                 (priority,
                                                  self.priorityValues.getList()))

    # =========================================================================
    def _createPList(self, name=None):
        """Create a new PListFunction instance.

        It creates a new PListFunction instance to be used inside a trigger
        information dictionary with the instance priorities and defaultPriority
        values.

        >>> nt = Notificator((1, 2, 3), 2)

        >>> pl = nt._createPList('custom plist')
        >>> pl # doctest: +ELLIPSIS
        <plist.PListFunction object at 0x...>

        >>> pl.priorityValues.getList()
        (1, 2, 3)

        >>> pl.priorityValues.getDefault()
        2

        >>> pl.name
        'custom plist'

        :rtype: plist.PListFunction
        :return:
            A PListFunction instance using the list of priorities and the
            default value for the notify manager instance.
        """
        return plist.PListFunction(self.priorityValues.getList(),
                                   self.priorityValues.getDefault(),
                                   name=name)

    # =========================================================================
    def _getRegistrationSideFromFlag(self, isBeforeFlag):
        """Return string used for searching in priority list dictionary.

        It translate the boolean flag to the string with the correct key
        in the priority list dictionary.

        >>> nt = Notificator((1, 2, 3), 2)

        >>> nt._getRegistrationSideFromFlag(True)
        'before'

        >>> nt._getRegistrationSideFromFlag(False)
        'after'

        :type isBeforeFlag: boolean
        :param isBeforeFlag:
            If True, then return string used for inserting 'before.
            If False, then return string used for inserting after.
            .
        :rtype: str
        :return:
            If True returns 'before' string. If False return 'after' string.
        """
        return BEFORE if isBeforeFlag else AFTER

    # =========================================================================
    def registerTrigger(self, triggerFunction, *args, **kwargs):
        """Register a new trigger function.

        It registers a new custom trigger function, where notification can be
        registered later on, and they will be called when the trigger function
        is called.

        >>> nt = Notificator((1, 2, 3), 2)

        >>> def trigger(): pass
        >>> nt.registerTrigger(trigger) # doctest: +ELLIPSIS
        {'trigger': <function trigger at 0x...>, 'id': 1}

        >>> nt.triggerInfo[1] # doctest: +ELLIPSIS
        {'trigger': <function trigger at 0x...>, 'plist': {'after': <plist.PListFunction object at 0x...>, 'before': <plist.PListFunction object at 0x...>}, 'args': (), 'kwargs': {}}

        :type triggerFunction: function
        :param triggerFunction:
            Custom trigger function to be registered.

        :type args: list
        :param args:
            Default list parameters when the trigger function is called.

        :type kwargs: dict
        :param kwargs:
            Default dictionary parameters when the trigger function is called.

        :rtype: dict
        :return:
            It return a dictionary with key 'id' with the id for the
            registered trigger and key 'trigger' with the wrapped up method
            that should be called now.

        :raise RegistrationException:
            Registration exception if the trigger method was not registered
            properly.
        """
        try:
            self._validateMethodCall(triggerFunction)
            id = self._increaseId()

            ## TODO - MOVED - This has been moved to _validateMethodCall
            ## function.
            ## # This is required for testing with Mock functions, because
            ## # they are required to have a __name__ attribute in order to
            ## # work with @functools.wraps decorator.
            ## if isinstance(triggerFunction, mock.Mock):
            ##    triggerFunction.__name__ = triggerFunction._mock_name

            # =================================================================
            @functools.wraps(triggerFunction)
            def _wrapTrigger(*args, **kwargs):
                """Wrapped up the trigger function.

                It wraps up the custom trigger function, so notification can
                be called when the trigger function is executed.

                :type args: list
                :param args: Default list parameters when the trigger function
                is called.

                :type kwargs: dict
                :param kwargs: Default dictionary parameters when the trigger
                function is called.

                :rtype: function
                :return: Return trigger function return value.
                """
                triggerInfo = self.triggerInfo[id]
                argsToUse   = args if args  else triggerInfo[ARGS]
                kwargsToUse = kwargs if kwargs else triggerInfo[KWARGS]
                if __debug__:
                    self.logger.debug('triggerFunction %s, argsToUse %s, kwargsToUse %s' %
                                      (triggerInfo[TRIGGER], argsToUse, kwargsToUse))
                triggerInfo[PLIST][BEFORE].callForAll(*argsToUse, **kwargsToUse)
                retvalue = triggerFunction(*argsToUse, **kwargsToUse)
                triggerInfo[PLIST][AFTER].callForAll(*argsToUse, **kwargsToUse)
                return retvalue

            self.triggerInfo[id] = {TRIGGER: _wrapTrigger, ARGS: args, KWARGS: kwargs,
                                    PLIST: {BEFORE: self._createPList('BEFORE'), AFTER: self._createPList('AFTER')}}
            if __debug__:
                self.logger.debug('%s: register trigger %s with args %s and kwargs %s, id=%d' %
                                  (info.FUNC(), triggerFunction, args, kwargs, id))
            return {ID: id, TRIGGER: _wrapTrigger}
        except InvalidMethodCallException:
            self.logger.error('%s: Invalid Trigger Function: %s' %
                              (info.FUNC(), triggerFunction))
            raise RegistrationException()

    # =========================================================================
    def deregisterTrigger(self, id):
        """Deregister a given trigger at the given id.

        It proceeds to deregister the given trigger at the given id.

        :type id: int
        :param id:
            Id where the trigger is located.

        >>> nt = Notificator((1, 2, 3), 2)

        >>> def trigger(): pass
        >>> nt.registerTrigger(trigger) # doctest: +ELLIPSIS
        {'trigger': <function trigger at 0x...>, 'id': 1}

        >>> nt.triggerInfo[1] # doctest: +ELLIPSIS
        {'trigger': <function trigger at 0x...>, 'plist': {'after': <plist.PListFunction object at 0x...>, 'before': <plist.PListFunction object at 0x...>}, 'args': (), 'kwargs': {}}

        >>> nt.deregisterTrigger(1)

        >>> nt.triggerInfo[1]
        Traceback (most recent call last):
        ...
        KeyError: 1

        >>> nt.deregisterTrigger(1)
        Traceback (most recent call last):
        ...
        DeregistrationException: Deregistration failed : Invalid id value: 1

        :raise DeregistrationException:
            If the trigger was not deregistered for any reason.
        """
        try:
            if __debug__:
                self.logger.debug('%s: deregister trigger with id=%d' %
                                  (info.FUNC(), id))
            self._validateId(id)
            del self.triggerInfo[id]

        except InvalidIdException:
            raise DeregistrationException('Invalid id value: %s' % id)

    # =========================================================================
    def registerNotification(self,
                             id,
                             priority,
                             isBeforeFlag,
                             inFrontFlag,
                             notification,
                             *args, **kwargs):
        """Register notification to a trigger identified by the given id value.

        It registers the given notification with the given priority at the
        given position for a trigger which is identified by the given id value.

        >>> nt = Notificator((1, 2, 3), 2)

        >>> def trigger(): pass
        >>> nt.registerTrigger(trigger) # doctest: +ELLIPSIS
        {'trigger': <function trigger at 0x...>, 'id': 1}

        >>> def notif(): pass
        >>> nt.registerNotification(1, 1, True, True, notif)
        True

        >>> nt.registerNotification(2, 1, True, True, notif)
        Traceback (most recent call last):
        ...
        RegistrationException: Registration failed : Invalid id value: 2

        >>> nt.registerNotification(1, 1, True, True, 'NOTIF')
        Traceback (most recent call last):
        ...
        RegistrationException: Registration failed : Invalid notification method: NOTIF

        >>> nt.registerNotification(1, 0, True, True, notif)
        Traceback (most recent call last):
        ...
        RegistrationException: Registration failed : Invalid priority: 0 not in (1, 2, 3)

        :type id: int
        :param id:
            Identifies the trigger where the notification will be registered.

        :type priority: object
        :param priority:
            Notification priority.

        :type isBeforeFlag: boolean
        :param isBeforeFlag:
            If True, then Notification will be called before the trigger runs.
            If False, then Notification will be called after the trigger runs.

        :type inFrontFlag: boolean
        :param inFrontFlag:
            If True, then notification is registered at the front of the
            priority list.
            If False, then notification is registered at the back of the
            priority list.

        :type notification: function
        :param notification:
            Notification to be registered. It should be a method call.

        :type args: list
        :param args:
            List of parameters to pass when the notification is called.

        :type kwargs: dict
        :param kwargs:
            Dictionary of parameters to pass when the notification is called.

        :rtype: boolean
        :return:
            True if the notification was registered.

        :raise RegistrationException:
            Notification was not registered properly.
        """
        try:
            if __debug__:
                self.logger.debug('%s: register %s notification %s with args %s and kwargs %s, id=%d' %
                                  (info.FUNC(), BEFORE if isBeforeFlag else AFTER, notification, args, kwargs, id))
            self._validateId(id)
            self._validateMethodCall(notification)
            self._validatePriorityValue(priority)
            registrationSide = self._getRegistrationSideFromFlag(isBeforeFlag)
            triggerInfoPList = self.triggerInfo[id][PLIST]
            addNotificationToListMethod =\
                triggerInfoPList[registrationSide].addAtFront if inFrontFlag\
                else triggerInfoPList[registrationSide].addAtBack
            addNotificationToListMethod({METHOD: notification,
                                         ARGS: args,
                                         KWARGS: kwargs}, priority)
            return True

        except InvalidIdException:
            raise RegistrationException('Invalid id value: %s' % id)
        except InvalidMethodCallException:
            raise RegistrationException('Invalid notification method: %s' %
                                        notification)
        except plist.InvalidPriorityException:
            raise RegistrationException('Invalid priority: %s not in %s' %
                                        (priority,
                                         self.priorityValues.getList()))

    # =========================================================================
    def deregisterNotification(self,
                               id,
                               priority,
                               isBeforeFlag,
                               notification):
        """Deregister notification to a trigger identified by given id value.

        It deregisters the given notification with the given priority at the
        given position for a trigger which is identified by the given id value.

        >>> nt = Notificator((1, 2, 3), 2)

        >>> def trigger(): pass
        >>> nt.registerTrigger(trigger) # doctest: +ELLIPSIS
        {'trigger': <function trigger at 0x...>, 'id': 1}

        >>> def notif(): pass
        >>> nt.registerNotification(1, 1, True, True, notif)
        True

        >>> nt.deregisterNotification(1, 1, True, notif) # doctest: +ELLIPSIS
        <function notif at 0x...>

        >>> nt.deregisterNotification(2, 1, True, notif)
        Traceback (most recent call last):
        ...
        DeregistrationException: Deregistration failed : Invalid id value: 2

        >>> nt.deregisterNotification(1, 1, True, 'NOTIF')
        Traceback (most recent call last):
        ...
        DeregistrationException: Deregistration failed : Invalid notification method: NOTIF

        >>> nt.deregisterNotification(1, 0, True, notif)
        Traceback (most recent call last):
        ...
        DeregistrationException: Deregistration failed : Invalid priority: 0 not in (1, 2, 3)

        :type id: int
        :param id:
            Identifies the trigger where the notification will be registered.

        :type priority: object
        :param priority:
            Notification priority.

        :type isBeforeFlag: boolean
        :param isBeforeFlag:
            If True, then Notification will be called before the trigger runs.
            If False, then Notification will be called after the trigger runs.

        :type notification: function
        :param notification:
            Notification to be registered. It should be a method call.

        :rtype: boolean
        :return:
            True if the notification was deregistered.

        :raise DeregistrationException:
            Notification was not deregistered properly.
        """
        try:
            if __debug__:
                self.logger.debug('%s: deregister %s notification %s, id=%d' %
                                  (info.FUNC(),
                                   BEFORE if isBeforeFlag else AFTER,
                                   notification,
                                   id))
            self._validateId(id)
            self._validateMethodCall(notification)
            self._validatePriorityValue(priority)
            registrationSide = self._getRegistrationSideFromFlag(isBeforeFlag)
            triggerInfoPList = self.triggerInfo[id][PLIST]
            return triggerInfoPList[registrationSide].remove({METHOD: notification},
                                                             priority)

        except InvalidIdException:
            raise DeregistrationException('Invalid id value: %s' % id)
        except InvalidMethodCallException, plist.InvalidEntryException:
            raise DeregistrationException('Invalid notification method: %s' %
                                          notification)
        except plist.InvalidPriorityException:
            raise DeregistrationException('Invalid priority: %s not in %s' %
                                          (priority,
                                           self.priorityValues.getList()))

    # =========================================================================
    def runTrigger(self, id, *args, **kwargs):
        """Run the given trigger by the id.

        It runs the trigger with the given id, and it overrides the given
        args and kwargs.

        >>> nt = Notificator((1, 2, 3), 2)

        >>> def trigger1(): print 'the trigger1'
        >>> nt.registerTrigger(trigger1) # doctest: +ELLIPSIS
        {'trigger': <function trigger1 at 0x...>, 'id': 1}

        >>> nt.runTrigger(1)
        the trigger1

        >>> def trigger2(x, y=0): print 'the trigger2 with (%s, %s)' % (x, y)
        >>> nt.registerTrigger(trigger2) # doctest: +ELLIPSIS
        {'trigger': <function trigger2 at 0x...>, 'id': 2}

        >>> nt.runTrigger(2, 'two', y=2)
        the trigger2 with (two, 2)

        >>> def trigger3(x, y=0): print 'the trigger3 with (%s, %s)' % (x, y)
        >>> nt.registerTrigger(trigger3, 'THREE', y=3) # doctest: +ELLIPSIS
        {'trigger': <function trigger3 at 0x...>, 'id': 3}

        >>> nt.runTrigger(3)
        the trigger3 with (THREE, 3)

        >>> def trigger4(): print 'the trigger4'
        >>> nt.registerTrigger(trigger4) # doctest: +ELLIPSIS
        {'trigger': <function trigger4 at 0x...>, 'id': 4}

        >>> def notif1(): print 'notif1'
        >>> nt.registerNotification(4, 1, True, True, notif1)
        True

        >>> nt.runTrigger(4)
        notif1
        the trigger4

        >>> nt.runTrigger(0)
        Traceback (most recent call last):
        ...
        TriggerException: Trigger failed : Invalid id value: 0

        :type id: int
        :param id:
            Id where the trigger is located in the triggerInfo dictionary.

        :type args: list
        :param args:
                Override list parameters when the trigger function is called.

        :type kwargs: dict
        :param kwargs:
                Override dictionary parameters when the trigger function is called.

        :rtype: function
        :return:
            Trigger method return value.

        :raise TriggerException:
            If the trigger didn't run properly.
        """
        try:
            if __debug__:
                self.logger.debug('%s: running trigger with id=%d' %
                                  (info.FUNC(), id))
            self._validateId(id)
            triggerInfo = self.triggerInfo[id]
            triggerFunction = triggerInfo[TRIGGER]
            argsToUse       = args if args  else triggerInfo[ARGS]
            kwargsToUse     = kwargs if kwargs else triggerInfo[KWARGS]
            return triggerFunction(*argsToUse, **kwargsToUse)
        except InvalidIdException:
            raise TriggerException('Invalid id value: %s' % id)


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
    #mgr = Notificator((1, 2, 3), 2)
    #triggerMethod = lambda x: mgr.logger.info('trigger %s' % x)
    #notifMethod   = lambda x, y: mgr.logger.info('pre  Notif %s %s' % (x, y))
    #mgr.registerTrigger(triggerMethod, 'TRIGGER')
    #mgr.registerNotification(1, 2, True, True, notifMethod, 'PRE-NOTIF')
    #mgr.registerNotification(1, 2, False, True, notifMethod, 'POST-NOTIF')
    #import mockerator
    #mockerator.verbose = True
    #mockInstances = mockerator.attachMockeratorKlass(plist.PList, timeStamp=True)
    #for inst in mockInstances:
    #    mockerator.attachMethodToMockerator(inst, methods=('_callEntry', ), color={'co': 'CYAN', 'xground': 'FG'}, timeStamp=False)
    #mgr.runTrigger(1)
    #for inst in mockInstances:
    #    print inst.name, inst
    #    for lista in mockerator.getMethodCalls(inst):
    #        print lista
    import doctest
    doctest.testmod()
