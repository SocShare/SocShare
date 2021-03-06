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
        resp = c.post(reverse('socshare:register'),copy_modify(valid_registration,"email",non_valid_email))
        self.assertTrue(resp.context != None and resp.context["alert_msg"] == failure_message,"Accepting Registration with non valid email")

    """
    Testing the Registration function accepts vaild registrations and rejects double registrations
    """
    def test_register_vaild_email_twice(self):
        resp = c.post(reverse('socshare:register'),valid_registration)
        self.assertTrue(resp.context == None,"Registration not functioning despite having a vaild email")

        failure_message = "An account is already registered with this email address!"
        resp = c.post(reverse('socshare:register'),valid_registration)
        self.assertTrue(resp.context != None and resp.context["alert_msg"] == failure_message,"Fails to recognise that the email is already in the DB")

        # Asserts that the user has been registered
        self.assertTrue(login_with_vaild(),"Fails to login to the newly registered account")

    """
    Testing that registration function does not accept non matching passwords
    """
    def test_register_vaild_email_without_matching_passwords(self):
        failure_message =  "Passwords do not match!"
        resp = c.post(reverse('socshare:register'),copy_modify(valid_registration,"verify","test1"))
        self.assertTrue(resp.context != None and resp.context["alert_msg"] == failure_message,"Registration succeeds despite having non matching passwords")
        

    """
        Testing that registration function does not accept null fields
    """
    def test_register_vaild_email_with_nulls(self):
        suc,k = nulls_fuzzer(reverse('socshare:register'),valid_registration)
        self.assertTrue(suc,f"The first field to inccorrectly accept a null was {k}")
