from socshare.tests.tests_core import *

"""
    Testing the Registration function
"""
class CheckRegistration(TestCase):

    """
    Testing the Registration function rejects invalid emails
    """
    def test_register_not_vaild_email(self):
        failure_message = "Account not registered with SRC!"
        resp = c.post(reverse('socshare:register'),{"email":non_vaild_email,"password":'test',"verify":'test',"name":'This is a test',"acronym":'tiat'})
        self.assertTrue(resp.context != None and resp.context["alert_msg"] == failure_message)

    """
    Testing the Registration function accepts vaild registrations and rejects double registrations
    """
    def test_register_vaild_email_twice(self):
        resp = c.post(reverse('socshare:register'),{"email":vaild_email,"password":'test',"verify":'test',"name":'This is a test',"acronym":'tiat'})
        self.assertTrue(resp.context == None)

        failure_message = "An account is already registered with this email address!"
        resp = c.post(reverse('socshare:register'),{"email":vaild_email,"password":'test',"verify":'test',"name":'This is a test',"acronym":'tiat'})
        self.assertTrue(resp.context != None and resp.context["alert_msg"] == failure_message)

        # Asserts that the user has been registered
        self.assertTrue(c.login(username=slugify('This is a test'),password="test"))

    """
    Testing that registration function does not accept non matching passwords
    """
    def test_register_vaild_email_without_matching_passwords(self):
        failure_message =  "Passwords do not match!"
        resp = c.post(reverse('socshare:register'),{"email":vaild_email,"password":'test1',"verify":'test2',"name":'This is a test',"acronym":'tiat'})
        self.assertTrue(resp.context != None and resp.context["alert_msg"] == failure_message)
        

    """
        Testing that registration function does not accept null fields
    """
    def test_register_vaild_email_with_nulls(self):
        resp = c.post(reverse('socshare:register'),{"email":vaild_email,"password":'',"verify":'',"name":'',"acronym":''})
        self.assertTrue(resp.context != None and resp.context["alert_msg"] != None)
