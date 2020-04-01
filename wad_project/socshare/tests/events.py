from socshare.tests.tests_core import *

"""
Testing the Events Page, Events Editing and Events creation functionality
"""
class Events(TestCase):

    """
    Create an event then try an retrieve it from the DB
    """
    def test_create_events(self):
        resp = c.post(reverse('socshare:add_event'),valid_event)
        self.assertTrue(resp.context == None,"")

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