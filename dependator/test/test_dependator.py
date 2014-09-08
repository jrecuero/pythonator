#!/usr/bin/env python

"""
:author: Jose Carlos Recuero
:version: 1.0
:since: 08/20/2014

TestDependator contains all Pluginator unit tests.
"""


__docformat__ = "restructuredtext en"


###############################################################################
##  _                            _
## (_)_ __ ___  _ __   ___  _ __| |_ ___
## | | '_ ` _ \| '_ \ / _ \| '__| __/ __|
## | | | | | | | |_) | (_) | |  | |_\__ \
## |_|_| |_| |_| .__/ \___/|_|   \__|___/
##             |_|
###############################################################################
#                      _              _
#
# import std python modules
#
import unittest
import mock

#
# import user defined python modules
#
from dependator.state import State
import dependator.dependator as dep


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

# =============================================================================
def TestDependatorSuite():
    """ Unit test suite for runing Pluginator unit tests.
    """
    suite = unittest.TestSuite()
    suite.addTest(TestDependator('test_NotificationWithOneInstanceDependency'))
    suite.addTest(TestDependator('test_NotificationWithTwoInstanceDependency'))
    suite.addTest(TestDependator('test_NotificationNotCalledWhenDependencyRemoved'))
    suite.addTest(TestDependator('test_NotificationWithOneAttributeUpdate'))
    return suite


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
class TestDependator(unittest.TestCase):
    """ TestDependator class provides all unit test for Dependator class.
    """

    # =========================================================================
    def setUp(self):
        """Set up TestDependator unit test.

        It sets up all functionality required for running TestDependator.
        """
        self.dep = dep.Dependator()

    # =========================================================================
    def tearDown(self):
        """Tear down TestDependator unit test.

        It tears down all funcionality created when the test was set up.
        """
        pass

    # =========================================================================
    def test_NotificationWithOneInstanceDependency(self):
        """
        Test Basic notifications being triggered by dependator when only one
        instance is passed in the dependency list
        """
        self.dep.registerInstance('ONE:1')
        self.dep.registerInstance('TWO:2')

        notification = mock.Mock()
        self.dep.setDependency('ONE:1', ('TWO:2', ), {State.NONE:    notification.none,
                                                      State.CREATED: notification.created,
                                                      State.ACTIVED: notification.actived,
                                                      State.WAITING: notification.waiting,
                                                      State.PAUSED:  notification.paused,
                                                      State.DELETED: notification.deleted, })

        self.dep.notifyCreated('ONE:1')
        self.assertFalse(notification.none.called)
        self.assertFalse(notification.created.called)
        self.assertFalse(notification.actived.called)
        self.assertFalse(notification.waiting.called)
        self.assertFalse(notification.paused.called)
        self.assertFalse(notification.deleted.called)

        notification.reset_mock()

        self.dep.notifyCreated('TWO:2')
        self.assertFalse(notification.none.called)
        self.assertTrue(notification.created.called)
        self.assertFalse(notification.actived.called)
        self.assertFalse(notification.waiting.called)
        self.assertFalse(notification.paused.called)
        self.assertFalse(notification.deleted.called)

        notification.reset_mock()

        self.dep.notifyActived('TWO:2')
        self.assertFalse(notification.none.called)
        self.assertFalse(notification.created.called)
        self.assertTrue(notification.actived.called)
        self.assertFalse(notification.waiting.called)
        self.assertFalse(notification.paused.called)
        self.assertFalse(notification.deleted.called)

        notification.reset_mock()

        self.dep.notifyWaiting('TWO:2')
        self.assertFalse(notification.none.called)
        self.assertFalse(notification.created.called)
        self.assertFalse(notification.actived.called)
        self.assertTrue(notification.waiting.called)
        self.assertFalse(notification.paused.called)
        self.assertFalse(notification.deleted.called)

        notification.reset_mock()

        self.dep.notifyPaused('TWO:2')
        self.assertFalse(notification.none.called)
        self.assertFalse(notification.created.called)
        self.assertFalse(notification.actived.called)
        self.assertFalse(notification.waiting.called)
        self.assertTrue(notification.paused.called)
        self.assertFalse(notification.deleted.called)

        notification.reset_mock()

        self.dep.notifyDeleted('TWO:2')
        self.assertFalse(notification.none.called)
        self.assertFalse(notification.created.called)
        self.assertFalse(notification.actived.called)
        self.assertFalse(notification.waiting.called)
        self.assertFalse(notification.paused.called)
        self.assertTrue(notification.deleted.called)

        notification.reset_mock()

        self.dep.notifyDestroyed('TWO:2')
        self.assertTrue(notification.none.called)
        self.assertFalse(notification.created.called)
        self.assertFalse(notification.actived.called)
        self.assertFalse(notification.waiting.called)
        self.assertFalse(notification.paused.called)
        self.assertFalse(notification.deleted.called)

    # =========================================================================
    def test_NotificationWithTwoInstanceDependency(self):
        """
        Test Basic notifications being triggered by dependator when two
        instances are passed in the dependency list
        """
        self.dep.registerInstance('ONE:1')
        self.dep.registerInstance('TWO:2')
        self.dep.registerInstance('THREE:3')

        notification = mock.Mock()
        self.dep.setDependency('ONE:1',
                               ('TWO:2', 'THREE:3'),
                               {State.NONE:    notification.none,
                                State.CREATED: notification.created,
                                State.ACTIVED: notification.actived,
                                State.WAITING: notification.waiting,
                                State.PAUSED:  notification.paused,
                                State.DELETED: notification.deleted, })

        self.dep.notifyCreated('TWO:2')
        self.assertFalse(notification.none.called)
        self.assertFalse(notification.created.called)
        self.assertFalse(notification.actived.called)
        self.assertFalse(notification.waiting.called)
        self.assertFalse(notification.paused.called)
        self.assertFalse(notification.deleted.called)

        notification.reset_mock()

        self.dep.notifyCreated('THREE:3')
        self.assertFalse(notification.none.called)
        self.assertTrue(notification.created.called)
        self.assertFalse(notification.actived.called)
        self.assertFalse(notification.waiting.called)
        self.assertFalse(notification.paused.called)
        self.assertFalse(notification.deleted.called)

        notification.reset_mock()

        self.dep.notifyActived('TWO:2')
        self.assertFalse(notification.none.called)
        self.assertFalse(notification.created.called)
        self.assertFalse(notification.actived.called)
        self.assertFalse(notification.waiting.called)
        self.assertFalse(notification.paused.called)
        self.assertFalse(notification.deleted.called)

        notification.reset_mock()

        self.dep.notifyActived('THREE:3')
        self.assertFalse(notification.none.called)
        self.assertFalse(notification.created.called)
        self.assertTrue(notification.actived.called)
        self.assertFalse(notification.waiting.called)
        self.assertFalse(notification.paused.called)
        self.assertFalse(notification.deleted.called)

        notification.reset_mock()

        self.dep.notifyWaiting('TWO:2')
        self.assertFalse(notification.none.called)
        self.assertFalse(notification.created.called)
        self.assertFalse(notification.actived.called)
        self.assertFalse(notification.waiting.called)
        self.assertFalse(notification.paused.called)
        self.assertFalse(notification.deleted.called)

        notification.reset_mock()

        self.dep.notifyWaiting('THREE:3')
        self.assertFalse(notification.none.called)
        self.assertFalse(notification.created.called)
        self.assertFalse(notification.actived.called)
        self.assertTrue(notification.waiting.called)
        self.assertFalse(notification.paused.called)
        self.assertFalse(notification.deleted.called)

        notification.reset_mock()

        self.dep.notifyPaused('TWO:2')
        self.assertFalse(notification.none.called)
        self.assertFalse(notification.created.called)
        self.assertFalse(notification.actived.called)
        self.assertFalse(notification.waiting.called)
        self.assertFalse(notification.paused.called)
        self.assertFalse(notification.deleted.called)

        notification.reset_mock()

        self.dep.notifyPaused('THREE:3')
        self.assertFalse(notification.none.called)
        self.assertFalse(notification.created.called)
        self.assertFalse(notification.actived.called)
        self.assertFalse(notification.waiting.called)
        self.assertTrue(notification.paused.called)
        self.assertFalse(notification.deleted.called)

        notification.reset_mock()

        self.dep.notifyDeleted('TWO:2')
        self.assertFalse(notification.none.called)
        self.assertFalse(notification.created.called)
        self.assertFalse(notification.actived.called)
        self.assertFalse(notification.waiting.called)
        self.assertFalse(notification.paused.called)
        self.assertFalse(notification.deleted.called)

        notification.reset_mock()

        self.dep.notifyDeleted('THREE:3')
        self.assertFalse(notification.none.called)
        self.assertFalse(notification.created.called)
        self.assertFalse(notification.actived.called)
        self.assertFalse(notification.waiting.called)
        self.assertFalse(notification.paused.called)
        self.assertTrue(notification.deleted.called)

        notification.reset_mock()

        self.dep.notifyDestroyed('TWO:2')
        self.assertFalse(notification.none.called)
        self.assertFalse(notification.created.called)
        self.assertFalse(notification.actived.called)
        self.assertFalse(notification.waiting.called)
        self.assertFalse(notification.paused.called)
        self.assertFalse(notification.deleted.called)

        notification.reset_mock()

        self.dep.notifyDestroyed('THREE:3')
        self.assertTrue(notification.none.called)
        self.assertFalse(notification.created.called)
        self.assertFalse(notification.actived.called)
        self.assertFalse(notification.waiting.called)
        self.assertFalse(notification.paused.called)
        self.assertFalse(notification.deleted.called)

    # =========================================================================
    def test_NotificationNotCalledWhenDependencyRemoved(self):
        """
        Test dependator does not trigger any callback whe dependecy is removed
        """
        self.dep.registerInstance('ONE:1')
        self.dep.registerInstance('TWO:2')

        notification = mock.Mock()
        id = self.dep.setDependency('ONE:1', ('TWO:2', ), {State.NONE:    notification.none,
                                                           State.CREATED: notification.created,
                                                           State.ACTIVED: notification.actived,
                                                           State.WAITING: notification.waiting,
                                                           State.PAUSED:  notification.paused,
                                                           State.DELETED: notification.deleted, })

        self.dep.notifyCreated('TWO:2')
        self.assertTrue(notification.created.called)

        self.dep.clearDependency(id)

        notification.reset_mock()

        self.dep.notifyActived('TWO:2')
        self.assertFalse(notification.none.called)
        self.assertFalse(notification.created.called)
        self.assertFalse(notification.actived.called)
        self.assertFalse(notification.waiting.called)
        self.assertFalse(notification.paused.called)
        self.assertFalse(notification.deleted.called)

    # =========================================================================
    def test_NotificationWithOneAttributeUpdate(self):
        """
        Test dependator trigger attribute update notications
        """
        self.dep.registerInstance('ONE:1')
        self.dep.registerInstance('TWO:2')

        notification = mock.Mock()
        result = self.dep.registerAttributeUpdate('ONE:1', 'TWO:2', 'x', notification.attribute_x)
        self.assertIsNotNone(result)

        self.dep.updateAttribute('TWO:2', 'x')
        self.assertTrue(notification.attribute_x.called)


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
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(TestDependatorSuite())
