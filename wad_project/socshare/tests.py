# To check the SRC checks are functioning correctly

# Vaild email: pausegaminglan@gmail.com
# Not Vaild Email: example@example.co.uk

from django.test import TestCase

from socshare.utils.src import check_email

from django.test import Client

from django.urls import reverse, resolve

vaild_email = "pausegaminglan@gmail.com"
non_vaild_email = "example@example.co.uk"

c = Client()


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

"""
Testing the Events Page, Events Editing and Events creation functionality
"""
class Events(TestCase):

    """
    Create an event then try an retrieve it from the DB
    """
    def test_create_events(self):
        pass

    """
    Edit an event then try an retrieve it from the DB
    """
    def test_edit_events(self):
        pass

    """
    Test the events page's ability to render events
    """
    def test_events_page(self):
        pass


    """
    Remove an event then try an retrieve it from the DB
    """
    def test_remove_events(self):
        pass