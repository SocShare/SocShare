from socshare.tests.tests_core import *

from socshare.models import Event

"""
Testing the Events Page, Events Editing and Events creation functionality
"""
class Events(TestCase):

    """
    Create an event then try an retrieve it from the DB
    """
    def test_create_events(self):
        # login_with_vaild()
        print(c.login(username=slugify(valid_login["username"]),password=valid_login["password"]))
        resp = c.post(reverse('socshare:add_event'),valid_event)
        print(resp)
        self.assertTrue(resp.context == None,"")
        event = Event.objects.filter(slug=slugify(valid_event["name"])).get()

    """
    Edit an event then try an retrieve it from the DB
    """
    def test_edit_events(self):
        resp = c.post(reverse('socshare:edit_event',kwargs={"event_slug":slugify(valid_event["name"])}),copy_modify(valid_event,"description","CANCELLED DUE TO COVID-19"))
        self.assertTrue(resp.context == None,"")

    """
    Test the events page's ability to render events
    """
    def test_events_page(self):
        pass

    """
    Tests the page for an individual event
    """
    def test_event_page(self):
        pass

    """
    Remove an event then try an retrieve it from the DB
    """
    def test_create_events_fuzz(self):
        suc,k = nulls_fuzzer(reverse('socshare:add_event'),valid_event,required_mask={"url":0})
        self.assertTrue(suc,f"The first field to inccorrectly accept a null was {k}")

    """
    Remove an event then try an retrieve it from the DB
    """
    def test_remove_events(self):
        pass