from socshare.utils.src import check_email

from socshare.tests.tests_core import *


"""
Tests the SRC test
"""
class SRCCheckTest(TestCase):

    """
    Tests to see if the check_email function is working correctly.
    """
    def test_SRC_Check(self):
        self.assertTrue(check_email("pausegaminglan@gmail.com"))
        self.assertFalse(check_email("example@example.co.uk"))