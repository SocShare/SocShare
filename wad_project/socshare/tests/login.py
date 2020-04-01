from socshare.tests.tests_core import *

"""
Testing the login and logout functionality of the site
"""
class SocietyLoginAndLogout(TestCase):

    """
    Login to a page and verify that the session is vaild
    """
    def test_login(self):
        c.post(reverse('socshare:register'),{"email":vaild_email,"password":'test',"verify":'test',"name":'This is a test',"acronym":'tiat'})
        resp = c.post(reverse('socshare:login'),{"email":vaild_email,"password":'test'})
        self.assertTrue(resp.context == None)
        self.assertTrue(c.login(username=slugify('This is a test'),password="test"))
        
    """
    Logout of a page and verify that the session has ended
    """
    def test_logout(self):
        resp = c.get(reverse('socshare:logout'))
        self.assertTrue(resp.context == None)