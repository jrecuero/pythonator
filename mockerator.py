#!/usr/bin/env python


"""
:author: Jose Carlos Recuero
:version: 1.0
:since: 08/13/2013

Mockerator functionality, which allows to mock and/or trace any instance.

It allows to trace all calls for the instance that is being mockerated. It
not only traces calls from other objects, but even calls done inside the
mockerated instance, if those methods are being mockerated, of course.

Methods could be fully mocked, so they are not calling any real
implementation, which could be useful when instance wants to be just
mocked up.

When instance is mockerated, a new mock.Mock attribute with
MOCK_INST_ATTR_NAME name is added to the instance. This attribute will be
the one storing all calls mockerated.

Interface provides parameters with a list of methods to be mockerated, so
instead of going to the full list of instance methods, only methods in
that dictionary will be mockerated. Even more, a new implementation could
be provided at that time (as the dictionary value, where the key is the
method name), so that new implementation will be the one being called.

Interface allows to define a list of methods that will not be mockerated,
so those calls will not be traced either.
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

from functools import WRAPPER_ASSIGNMENTS
import datetime
import gc

#
# import user python modules
#
import mock
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

MOCK_INST_ATTR_NAME = 'mockInst'
"""
:type: str
:var: Attribute name to be added to every instance to be mockerated. It
      contains the Mock instance which will track all instance calls.
"""

ORIG_METHOD_ATTR_NAME = 'method'
"""
:type: str
:var: Attribute name where the original class method will be stored in the
      mock wrapper function.
"""

BAK_ORIG_METHOD_ATTR_SUFIX = '_BAK'
"""
:type: str
:var: Suffix used for the backup attribute name where original instance method
      is backed up.
"""

MOCK_METHOD_DICT_ATTR_NAME = '_mockAttrMethodDict'
"""
:type: str
:var: Attribute name where the dictionary the mocked methods are stored.
"""

RETURN_VALUE_PATTERN = 'retoValue'
"""
:type: str
:var: Pattern used to store method traced return values. This are stored in
      the mock instances as calls just after the method being traced, so it is
      easy to keep tracking that information. Return value is passed as the
      only parameter for that call. This call has to be removed when method
      calls are returned.
"""

verbose = False
"""
:type: bool
:var: Flag to display log information.
"""

logger = loggerator.getLoggerator('mockerator')
"""
:type: loggerator.Loggerator
:var: Variable for local logger. Disable debug logs by default.
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

# =============================================================================
def invertXGround(xground):
    if xground == 'BG':
        return 'FG'
    else:
        return 'BG'


# =============================================================================
def logDebug(txt, colour=None, mode='FG', flag=False):
    if flag or verbose:
        logger.debug(txt, colour, mode)


# =============================================================================
def logInfo(txt, colour=None, mode='FG', flag=False):
    if flag or verbose:
        logger.info(txt, colour, mode)


# =============================================================================
def logError(txt, colour=None, mode='FG', flag=True):
    if flag:
        logger.error(txt, colour, mode)


# =============================================================================
def mockerator(instance,
               methodName,
               mockFuncFlag=False,
               timeStamp=True,
               preMethod=None,
               postMethod=None,
               color=None,
               watermark=None):
    """ Mockerator decorator.

    When a method is mockerated, the call is registered in the Mock attribute
    which was added when the mockerate was attached.

    If mockFuncFlag is False, the instance method is called as in a normal
    scenario, but is that flag is True, the method is fully mocked and it
    will not call its implementation.

    Instance method is placed in the wrapper attribute 'method', so it can
    be called later on.

    :type instance: object
    :param instance: instace which method will be added a mockerator.

    :type methodName: string
    :param methodName: method where mockerator will be applied.

    :type mockFuncFlag: bool
    :param mockFuncFlag: if True, method will be fully mocked, if False,
        them, call will be stored in the mock instance, but real method
        will be called and executed.

    :type timeStamp: bool
    :param timeStamp: if True, timestamp is added for all traces, if False
        time stamp is not added.

    :type preMethod: function
    :param preMethod: Method to be called before the instance method.

    :type postMethod: function
    :param postMethod: Method to be called after the instance method.j

    :type color: dict
    :param color: Dictionary with color and foreground/background to use.

    :type watermark: string
    :param watermark: Pattern to be logged at the start of the line.
    """

    def mockWrapper(*args, **kwargs):
        """ Mockerator decorator wrapper.

        :type args: list
        :param args: List of arguments to be passed to the method.

        :type kwargs: dict
        :param kwargs: Dictionary of arguments to be passed to the method.
        """
        pattern      = "[%s] Mockerator" % (watermark, ) if watermark else "Mockerator"
        retoValue     = None
        mockInstance = getattr(instance, MOCK_INST_ATTR_NAME, None)
        if not mockInstance:
            func = getattr(instance, methodName)
            retoValue = func(*args, **kwargs)
            return retoValue

        mockTimeNow  = "[%s] " % (datetime.datetime.now(), )
        if preMethod:
            logInfo('%s %s %s.%s (%s, %s)' %
                    (mockTimeNow, pattern, instance.__class__.__name__,
                        methodName, args, kwargs), color['co'], color['xground'])
            reto = preMethod(*args, **kwargs)
            if reto:
                if 'args' in reto and reto['args']:
                    args = reto['args']
                if 'kwargs' in reto and reto['kwargs']:
                    kwargs = reto['kwargs']
        # This is the Mock call: mockInstance.methodName(*args, **kwargs)
        mockArgs = [mockTimeNow] if timeStamp else []
        mockArgs.extend(args)
        getattr(mockInstance, methodName, None)(*mockArgs, **kwargs)
        logInfo('%s %s %s.%s (%s, %s)' %
                (mockTimeNow, pattern, instance.__class__.__name__,
                    methodName, args, kwargs), color['co'], color['xground'])
        if not mockFuncFlag:
            func = getattr(getattr(instance, methodName), ORIG_METHOD_ATTR_NAME)
            retoValue = func(*args, **kwargs)
        else:
            logInfo('%s %s I am mocking %s.%s (%s, %s)' %
                    (mockTimeNow, pattern, instance.__class__.__name__,
                        methodName, args, kwargs), color['co'], invertXGround(color['xground']))
        if postMethod:
            reto = postMethod(retoValue, *args, **kwargs)
            retoValue = reto if reto else retoValue

        getattr(mockInstance, RETURN_VALUE_PATTERN, None)(retoValue, methodName, *args, **kwargs)
        return retoValue

    color = {'co': 'GREEN', 'xground': 'FG'} if color is None else color
    # Save the instance method inside a wrapper attribute in order to be
    # able to called inside the wrapper call.
    originalMethod = getattr(instance, methodName, None)
    setattr(mockWrapper, ORIG_METHOD_ATTR_NAME, originalMethod)
    # Keep function name and docstring for the instance method untouched.
    for attr in WRAPPER_ASSIGNMENTS:
        originalAttr = getattr(originalMethod, attr, None)
        setattr(mockWrapper, attr, originalAttr)
    return mockWrapper


# =============================================================================
def _includeInternalMethod(attrName, inIncludeMethod):
    """ Check if internal method should be processed.

    By default internal method will not be mockerated, unless it is forced by
    passed the method in the includeMethod attribute.

    :type attrName: str
    :param attrName: name of the attribute being processed

    :type inIncludeMethod: bool
    :param inIncludeMethodL If True, the method was passed in the include
        method parameter, so it has to be included to be mockerated.

    :rtype: bool
    :return: True if method is not internal of is forced to be mockerated.
        False if the methos is internal and it is not forced to be mockerated.
    """
    return inIncludeMethod or not attrName.startswith('_')


# =============================================================================
def _getMethodEntryInDict(instance,
                          attrName,
                          mockFuncFlag=False,
                          inIncludeMethod=False):
    """ Generate an entry dictionary with method and flag.

    It generates a single entry for the dictionary where all methods to
    be mockerated.

    :attention:
        All internal methods are not mockered (methods that start with '_'.

    The first entry in the dictionary 'method' contains the instance method
    that will be finally executed by the wrapped after the call has been
    traced.

    The second entry in the dictionary is a flag that indicates if the method
    should be just traced (False) or fully mocked (True).

    :type instance: object
    :param instance: Instance to be mockerated.

    :type attrName: str
    :param attrName: name of the attribute being processed

    :type includeMethods: list, tuple, dict or None
    :param includeMethods: List/Tuple/Dictionary with methods to be mockerated.
        Only these methods will be mockerated, any other instance method will
        be excluded. Dictionary keys are method names and value could be None
        or it could a custom method replacing the instance method, it means,
        that will be the method to be called instead of the instance method.

    :type mockFuncFlag: bool
    :param mockFuncFlag: if True, all instance methods will be fully
        mocked, if False, them, call will be stored in the mock instance,
        but real method will be called and executed.

    :rtype: dict
    :return: Dictionary containing  'method' as the instance method attribute
    and 'flag' as a boolean showing is method is mocked or really called.
    """
    attr = getattr(instance, attrName)
    #if attrName == '__init__' or\
    #if not attrName.startswith('_') and\
    if _includeInternalMethod(attrName, inIncludeMethod) and\
            hasattr(attr, '__call__') and\
            not isinstance(attr, mock.Mock):
        return {'method': attr, 'flag': mockFuncFlag}
    else:
        return None


# =============================================================================
def _getBackupMethodName(attrName):
    """ Build backup attribute name.

    It returns the name for the attribute where the original instance method
    is backed up when a new method is provided when attached to the mockerator.

    :type attrName: str
    :param attrName: Attribute name
    """
    return '%s%s' % (attrName, BAK_ORIG_METHOD_ATTR_SUFIX)


# =============================================================================
def _getAttrNameFromBackupAttr(bakAttrName):
    """ Return attribute name for a backup attribute.

    It returns the attribute name for a backup attribute. The attribute name
    is the attribute where the original method was placed and it was store
    in the backup attribute.

    :type bakAttrName: str
    :param bakAttrName: Backup attribute name
    """
    try:
        return bakAttrName[:bakAttrName.index(BAK_ORIG_METHOD_ATTR_SUFIX)]
    except ValueError:
        return None


# =============================================================================
def _replaceInstanceAttrMethod(instance, attrName, newAttr):
    """ Replace a instance method attribute.

    It replaces an instance method attribute with a new one. It cares if that
    attribute has been already replaced in order to don't loose the original
    value.

    :type instance: object
    :param instance: Instance to be mockerated.

    :type attrName: str
    :param attrName: Instance attribute name being replaced.

    :type newAttr: func
    :param newAttr: New method replacing instance attribute.
    """
    oldAttr = getattr(instance, attrName, None)
    # At this point the backup attribute could be filled with
    # a value, that should be the original method, because it
    # was overwritten with a new method. If we decide to
    # overwrite again the same method, the backup attribute
    # should be preserved with the orignal instance method,
    # and the instance attribute with the previously overwriten
    # method will be lost with the new one.
    if not getattr(instance, _getBackupMethodName(attrName), None):
        methodAlreadyProcessed =\
            getattr(instance, MOCK_METHOD_DICT_ATTR_NAME, None)
        # If method was not backup but it was mockerated before,
        # then it has to backup the original method, which can
        # be found in the wrapper function attribute.
        if methodAlreadyProcessed and\
                attrName in methodAlreadyProcessed:
            # This method was already mockerated, so the
            # attribute we get here is the wrapper method,
            # so the original will be stored in the
            # ORIG_METHOD_ATTR_NAME attribute of the wrapper.
            oldAttr = getattr(oldAttr, ORIG_METHOD_ATTR_NAME, None)

        # oldAttr should contain the original instance method
        # at this point always.
        setattr(instance, _getBackupMethodName(attrName), oldAttr)

    # Overwrite the attribute method with the one given.
    setattr(instance, attrName, newAttr)


# =============================================================================
def generateSequenceToProcess(walkingSequence, dirKlass):
    """ Generate the sequence of attributes that has to be processed.

    It check is any wildcard was passed in order to look for methods that match
    with the pattern.

    :type walkingSequence: list
    :param walkingSequence: List with all attributes to be matched.

    :type dirKlass: list
    :param dirKlass: List with all attributes for the class.

    :rtype: list
    :return: List with all class attributes that have to be processed.
    """
    sequenceToProcess = []
    for attrName in walkingSequence:
        if '*' in attrName:
            attrName = attrName[0:-1]
            for klassAttrName in dirKlass:
                if klassAttrName.startswith(attrName):
                    sequenceToProcess.append(klassAttrName)
        else:
            sequenceToProcess.append(attrName)
    return sequenceToProcess


# =============================================================================
def generateMethodsToProcess(instance,
                             includeMethods=None,
                             excludeMethods=None,
                             mockFuncFlag=False):
    """ Generate a dictionary with attribute to be mockerated.

    This method process input parameters given and all instance attributes
    in order to generate a dictionary with methods to be mockerated, and if
    the have to be fully mocked or just traced.

    If a new method is provided, the original method will be stored in a new
    attribute with the same name and the suffix '_BAK'.

    :type instance: object
    :param instance: Instance to be mockerated.

    :type includeMethods: list, tuple, dict or None
    :param includeMethods: List/Tuple/Dictionary with methods to be mockerated.
        Only these methods will be mockerated, any other instance method will
        be excluded. Dictionary keys are method names and value could be None
        or it could a custom method replacing the instance method, it means,
        that will be the method to be called instead of the instance method.

    :type excludeMethods: list
    :param excludeMethods: List of methods which will not be mockerated.

    :type mockFuncFlag: bool
    :param mockFuncFlag: if True, all instance methods will be fully
        mocked, if False, them, call will be stored in the mock instance,
        but real method will be called and executed.

    :rtype: dict
    :return: Dictionary where keys are methods being processed and value
    is other dictionary containing  'method' as the instance method attribute
    and 'flag' as a boolean showing is method is mocked or really called.
    """
    includeMethods   = includeMethods if includeMethods else []
    methodsToProcess = {}
    includeWalkingSequence = []
    excludeWalkingSequence = []
    processInclude   = False
    dirKlass         = dir(instance)
    if not includeMethods:
        includeWalkingSequence = dirKlass
    elif isinstance(includeMethods, list) or isinstance(includeMethods, tuple):
        includeWalkingSequence = includeMethods
    elif isinstance(includeMethods, dict):
        processInclude = True
        includeWalkingSequence = includeMethods.keys()

    includeSequence = generateSequenceToProcess(includeWalkingSequence, dirKlass)

    excludeWalkingSequence = excludeMethods if excludeMethods else {}
    excludeSequence = generateSequenceToProcess(excludeWalkingSequence, dirKlass)

    for attrName in includeSequence:
        flag  = mockFuncFlag
        entry = None
        if processInclude and includeMethods[attrName]:
            for value in includeMethods[attrName]:
                if isinstance(value, bool):
                    flag = value
                elif hasattr(value, '__call__'):
                    _replaceInstanceAttrMethod(instance, attrName, value)

        if not attrName in excludeSequence:
            # When method attribute values are returned by this method, any method
            # being replaced, has been replaced at this point, so the replacement
            # will be returned in the 'method' value.
            entry = _getMethodEntryInDict(instance,
                                          attrName,
                                          flag,
                                          attrName in includeMethods)
            if entry:
                methodsToProcess[attrName] = entry

    return methodsToProcess


# =============================================================================
def attachMockerator(instance,
                     includeMethods=None,
                     excludeMethods=None,
                     mockFuncFlag=False,
                     merge=False,
                     timeStamp=True,
                     preMethod=None,
                     postMethod=None,
                     mockInstance=None,
                     color=None,
                     watermark=None):
    """ Attach a mockerator to an instance.

    This method inspect every instance attribute searching for methods.
    Every method, if it is not an internal method, will be mockerated, it
    means a decorator will be added on top of the method, and that decorator
    will trace method call in a Mock instance which is already stored as an
    attribute in the instance.

    The dictionary with all methods to be mockered are stored in a new
    attribute called MOCK_METHOD_DICT_ATTR_NAME.

    :type instance: object
    :param instance: Instance to be mockerated.

    :type includeMethods: list, tuple, dict or None
    :param includeMethods: List/Tuple/Dictionary with methods to be mockerated.
        Only these methods will be mockerated, any other instance method will
        be excluded. Dictionary keys are method names and value could be None
        or it could a custom method replacing the instance method, it means,
        that will be the method to be called instead of the instance method.

    :type excludeMethods: list
    :param excludeMethods: List of methods which will not be mockerated.

    :type mockFuncFlag: bool
    :param mockFuncFlag: if True, all instance methods will be fully
        mocked, if False, them, call will be stored in the mock instance,
        but real method will be called and executed.

    :type merge: bool
    :param merge: if True, then new methods are being added to the already
        mockerated instance. If False, them, we have to created the
        mockerated instance.

    :type timeStamp: bool
    :param timeStamp: if True, timestamp is added for all traces, if False
        time stamp is not added.

    :type preMethod: function
    :param preMethod: Method to be called before the instance method.

    :type postMethod: function
    :param postMethod: Method to be called after the instance method.j

    :type mockInstance: mock.Mock
    :param mockInstance: Use this mock instance.

    :type color: dict
    :param color: Dictionary with color and foreground/background to use.

    :type watermark: string
    :param watermark: Pattern to be logged at the start of the line.

    """
    methodsToProcess = generateMethodsToProcess(instance,
                                                includeMethods,
                                                excludeMethods,
                                                mockFuncFlag)
    # If we are adding more methods to an existing mockerated instance, then,
    # we have to merge already mockerated methods with new ones. If instance
    # was not mockerated, then we proceed as if we where calling
    # attachMockerator method.
    if merge:
        getattr(instance, MOCK_METHOD_DICT_ATTR_NAME, None).update(methodsToProcess)
    else:
        setattr(instance, MOCK_METHOD_DICT_ATTR_NAME, methodsToProcess)
    logInfo('attach mockerator to instance %s' % (instance, ), 'BLUE', 'FG')
    for keyAttrName, value  in methodsToProcess.iteritems():
        logDebug('attach mockerator %s' % (keyAttrName, ), 'BLUE', 'BG')
        setattr(instance,
                keyAttrName,
                mockerator(instance,
                           keyAttrName,
                           mockFuncFlag=value['flag'],
                           timeStamp=timeStamp,
                           preMethod=preMethod,
                           postMethod=postMethod,
                           color=color,
                           watermark=watermark))
    if not merge:
        mockInstance = mockInstance if mockInstance else mock.Mock()
        setattr(instance, MOCK_INST_ATTR_NAME, mockInstance)


# =============================================================================
def attachMockeratorKlass(klass,
                          includeMethods=None,
                          excludeMethods=None,
                          mockFuncFlag=False,
                          merge=False,
                          timeStamp=True,
                          preMethod=None,
                          postMethod=None,
                          mockInstance=None,
                          color=None,
                          watermark=None):
    """ Attach a mockerator to an Class.

    Attach mockerator to every instance created for this class.

    :type klass: object
    :param klass: Clas to be mockerated.

    :type includeMethods: list, tuple, dict or None
    :param includeMethods: List/Tuple/Dictionary with methods to be mockerated.
        Only these methods will be mockerated, any other instance method will
        be excluded. Dictionary keys are method names and value could be None
        or it could a custom method replacing the instance method, it means,
        that will be the method to be called instead of the instance method.

    :type excludeMethods: list
    :param excludeMethods: List of methods which will not be mockerated.

    :type mockFuncFlag: bool
    :param mockFuncFlag: if True, all instance methods will be fully
        mocked, if False, them, call will be stored in the mock instance,
        but real method will be called and executed.

    :type merge: bool
    :param merge: if True, then new methods are being added to the already
        mockerated instance. If False, them, we have to created the
        mockerated instance.

    :type timeStamp: bool
    :param timeStamp: if True, timestamp is added for all traces, if False
        time stamp is not added.

    :type preMethod: function
    :param preMethod: Method to be called before the instance method.

    :type postMethod: function
    :param postMethod: Method to be called after the instance method.j

    :type mockInstance: mock.Mock
    :param mockInstance: Use this mock instance.

    :type color: dict
    :param color: Dictionary with color and foreground/background to use.

    :type watermark: string
    :param watermark: Pattern to be logged at the start of the line.

    """
    instList = []
    for obj in gc.get_objects():
        if isinstance(obj, klass):
            instList.append(obj)
            attachMockerator(obj,
                             includeMethods=includeMethods,
                             excludeMethods=excludeMethods,
                             mockFuncFlag=mockFuncFlag,
                             merge=merge,
                             timeStamp=timeStamp,
                             preMethod=preMethod,
                             postMethod=postMethod,
                             mockInstance=mockInstance,
                             color=color,
                             watermark=obj)
    return instList


# =============================================================================
def detachMockerator(instance):
    """ Detach mockerator from instance.

    It removes mockerator from the instance, so it has to be rolled back to
    its original configuration for all attributes.

    Any new attribute added will be removed, and attributes replaces will be
    rolled back to their original values.

    :type instance: object
    :param instance: Instance to be demockerated.

    :rtype: Mock
    :return: Returns the mock instace used by the mockerator.
    """
    # Retrieve all methods that have been processed/mockerated. It should
    # return a dictionary where all keys are attribute names for attributes
    # that have been mockerated.
    #methodsProcessed = getattr(instance, MOCK_METHOD_DICT_ATTR_NAME, None)
    logInfo('detach mockerator from instance %s' % (instance, ), 'BLUE', 'FG')

    detachMethodFromMockerator(instance, None)
    retValue = getMockInstance(instance)
    delattr(instance, MOCK_METHOD_DICT_ATTR_NAME)
    delattr(instance, MOCK_INST_ATTR_NAME)
    return retValue


# =============================================================================
def attachMethodToMockerator(instance,
                             methods=None,
                             mockFuncFlag=False,
                             timeStamp=True,
                             preMethod=None,
                             postMethod=None,
                             mockInstance=None,
                             color=None,
                             watermark=None):
    """ Attach methods to a mockerated instance.

    It replaces some instance methods for those provided in the given
    parameter.

    If the method was already replaced, it is overwritten by the new one.

    :type instance: object
    :param instance: Instance to be mockerated.

    :type methods: list, tuple, dict
    :param methods: List/Tuple/Dictionary with methods to be mockerated.
        Add these methods to be mockerated. Dictionary keys are method names
        and value could be None or it could a custom method replacing the
        instance method, it means, that will be the method to be called
        instead of the instance method.

    :type mockFuncFlag: bool
    :param mockFuncFlag: if True, all instance methods will be fully
        mocked, if False, them, call will be stored in the mock instance,
        but real method will be called and executed.

    :type timeStamp: bool
    :param timeStamp: if True, timestamp is added for all traces, if False
        time stamp is not added.

    :type preMethod: function
    :param preMethod: Method to be called before the instance method.

    :type postMethod: function
    :param postMethod: Method to be called after the instance method.j

    :type mockInstance: mock.Mock
    :param mockInstance: Use this mock instance.

    :type color: dict
    :param color: Dictionary with color and foreground/background to use.

    :type watermark: string
    :param watermark: Pattern to be logged at the start of the line.
    """
    if getattr(instance, MOCK_INST_ATTR_NAME, None) is None:
        attachMockerator(instance,
                         includeMethods=methods,
                         excludeMethods=None,
                         mockFuncFlag=mockFuncFlag,
                         timeStamp=timeStamp,
                         preMethod=preMethod,
                         postMethod=postMethod,
                         mockInstance=mockInstance,
                         color=color,
                         watermark=watermark)
    else:
        attachMockerator(instance,
                         includeMethods=methods,
                         excludeMethods=None,
                         mockFuncFlag=mockFuncFlag,
                         merge=True,
                         timeStamp=timeStamp,
                         preMethod=preMethod,
                         postMethod=postMethod,
                         mockInstance=mockInstance,
                         color=color,
                         watermark=watermark)


# =============================================================================
def detachMethodFromMockerator(instance, methods=None):
    """ Detach methods from a mockerated instance.

    Methods given are detached from the mockerator, so they will not be traced
    or mocked anymore.

    :type instance: object
    :param instance: Instance to be mockerated.

    :type methods: list
    :param methods: List of methods to be detached from the mockerator.
    """
    methodsProcessed = getattr(instance, MOCK_METHOD_DICT_ATTR_NAME, None)
    for attrName in [atName for atName in methodsProcessed.keys()
                     if methods is None or atName in methods]:
        attr = getattr(instance, attrName, None)
        # Original instance attribute value could be in two placed:
        # - If it was replaced, it will be in the backed attribute.
        # - If it has not been replaced, it will be in an attribute for the
        #   decorator wrapper function.
        if hasattr(instance, _getBackupMethodName(attrName)):
            newAttr = getattr(instance, _getBackupMethodName(attrName), None)
        else:
            newAttr = getattr(attr, ORIG_METHOD_ATTR_NAME)
        logDebug('detach mockerator %s' % (attrName, ), 'BLUE', 'BG')
        setattr(instance, attrName, newAttr)


# =============================================================================
def restoreMockInstance(instance, restoreAttrs, timeStamp=False):
    """ Restore mockerated method to their original behavior.

    When instance is mockerated, some attribute methods could be overritten
    with some new functionality. Original behavior is kept, so this method
    restore that original behavior back.

    Backup attribute used to store the original method is removed from the
    instance.

    :type instance: object
    :param instance: Instance to be mockerated.

    :type restoreAttrs: list
    :param restoreAttrs: List of attribute methods that should be restored
        to their original implementation. Only methods that were overritten
        when the instance was mockerated can be restored.

    :type timeStamp: bool
    :param timeStamp: if True, timestamp is added for all traces, if False
        time stamp is not added.
    """
    for attrName in restoreAttrs:
        if hasattr(instance, attrName) and\
                hasattr(instance, _getBackupMethodName(attrName)):
            # restore original attribute value
            setattr(instance, attrName,
                    getattr(instance, _getBackupMethodName(attrName)))
            delattr(instance, _getBackupMethodName(attrName))
            # mockerate with the attribute already restored
            setattr(instance, attrName, mockerator(instance,
                                                   attrName,
                                                   mockFuncFlag=False,
                                                   timeStamp=timeStamp))


# =============================================================================
def getMockInstance(instance):
    """ Return the Mock instance.

    It returns the Mock instance for an instance that has been mockerated.

    :type instance: object
    :param instance: Instance being mockerated.

    :rtype: mock.Mock
    :return: Mock instance used for mocking and tracing.
    """
    return getattr(instance, MOCK_INST_ATTR_NAME, None)


# =============================================================================
def getMockMethodDict(instance):
    """ Return the dictionary with all mocked methods.

    It returns the attribute that contains a dictionary with all methods that
    have been mockerated.

    :type instance: object
    :param instance: Instance being mockerated.

    :rtype: dict
    :return: dictionary with all mockerated methods.
    """
    return getattr(instance, MOCK_METHOD_DICT_ATTR_NAME, None)


# =============================================================================
def getMethodCalls(instance):
    """ Return all calls stored in the Mock instance.

    :type instance: object
    :param instance: Instance being mockerated.

    :rtype: list
    :return: List with all method calls traced.
    """
    mockInstance   = getMockInstance(instance)
    allMethodCalls = mockInstance.method_calls if mockInstance else None
    methodCalls    = []
    for methodCall in allMethodCalls:
        if not RETURN_VALUE_PATTERN in str(methodCall):
            methodCalls.append(methodCall)
    return methodCalls


# =============================================================================
def getReturnValueMethodCalls(instance):
    """ Return all return values for every call being traced.

    :type instance: object
    :param instance: Instance being mockerated.

    :rtype: list
    :return: List with all method calls return values.
    """
    mockInstance   = getMockInstance(instance)
    allMethodCalls = mockInstance.method_calls if mockInstance else None
    retoValues     = []
    for methodCall in allMethodCalls:
        if RETURN_VALUE_PATTERN in str(methodCall):
            retoValues.append(methodCall[1])
    return retoValues


# =============================================================================
def logMethodCalls(instance):
    """ Log all calls stored in the Mock instance.

    :type instance: object
    :param instance: Instance being mockerated.
    """
    logInfo('', 'MAGENTA', 'FG', flag=True)
    logInfo('Methods Called by instance [%s]' % (instance, ), 'MAGENTA', 'FG', flag=True)
    #logInfo('%s' % (getMethodCalls(instance), ), 'MAGENTA', 'FG', flag=True)
    for methodCall in getMethodCalls(instance):
        logInfo('%s' % (methodCall, ), 'MAGENTA', 'FG', flag=True)


# =============================================================================
def check(pattern, instance=None, tested=None, result=None):
    #import ipdb
    import traceback
    import sys
    import inspect
    try:
        result = result if result else set()
        tested = tested if tested else set()
        instance = instance if instance else sys.modules['__main__']
        for name in dir(instance):
            if name.startswith('__'):
                continue
            attr = getattr(instance, name, None)
            if attr is not None:
                #print 'testing %s' % attr
                #(inspect.ismodule(attr) and
                # not 'usr/lib/python' in inspect.getsourcefile(attr)) and\
                if not inspect.isclass(attr) and\
                        not inspect.isfunction(attr) and\
                        not inspect.isbuiltin(attr) and\
                        not isinstance(attr, list) and\
                        not isinstance(attr, tuple) and\
                        not isinstance(attr, dict) and\
                        not isinstance(attr, int) and\
                        not isinstance(attr, str) and\
                        not isinstance(attr, bool) and\
                        not isinstance(attr, float) and\
                        not isinstance(attr, file):
                    if hasattr(attr, pattern):
                        #print '***** %s.%s.callMe' % (instance, attr)
                        result.add(attr)
                    elif hasattr(attr, '__init__'):
                        #ipdb.set_trace()    # BREAKPOINT
                        #logInfo('>>>>>> %s %s %s %s' % (type(instance), instance, attr, tested))
                        if not str(attr) in tested:
                            tested.add(str(attr))
                            check(pattern, attr, tested, result)
    except TypeError as e:
        logError("TypeError [%s] : %s" % (e, traceback.format_exc().splitlines()[1]))
    return result


###############################################################################
##       _                     _       __ _       _ _   _
##   ___| | __ _ ___ ___    __| | ___ / _(_)_ __ (_) |_(_) ___  _ __  ___
##  / __| |/ _` / __/ __|  / _` |/ _ \ |_| | '_ \| | __| |/ _ \| '_ \/ __|
## | (__| | (_| \__ \__ \ | (_| |  __/  _| | | | | | |_| | (_) | | | \__ \
##  \___|_|\__,_|___/___/  \__,_|\___|_| |_|_| |_|_|\__|_|\___/|_| |_|___/
##
###############################################################################
#


###############################################################################
##                  _
##  _ __ ___   __ _(_)_ __
## | '_ ` _ \ / _` | | '_ \
## | | | | | | (_| | | | | |
## |_| |_| |_|\__,_|_|_| |_|
##
###############################################################################
#

if __name__ == '__main__':
    pass
