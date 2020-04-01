from socshare.tests.tests_core import *

"""
Testing the login and logout functionality of the site
"""
class SocietyLoginAndLogout(TestCase):

    """
    Login to a page and verify that the session is vaild
    """
    def test_login(self):
        c.post(reverse('socshare:register'),valid_registration)
        resp = c.post(reverse('socshare:login'),valid_login)
        self.assertTrue(resp.context == None)
        self.assertTrue(login_with_vaild())
        
    """
    Logout of a page and verify that the session has ended
    """
    def test_logout(self):
        resp = c.get(reverse('socshare:logout'))
        self.assertTrue(resp.context == None)

    """
    Login to a page and verify that the session is vaild
    """
    def test_login_with_nulls(self):
        suc,k = nulls_fuzzer(reverse('socshare:login'),valid_login)
        self.assertTrue(suc,f"The first field to inccorrectly accept a null was {k}")