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
        register_and_login()
        resp = c.post(reverse('socshare:add_event'),valid_event)
        self.assertTrue(resp.context == None,"")
        event = Event.objects.filter(slug=slugify(valid_event["name"])).get()
        self.assertTrue(event.name == valid_event["name"])

    """
    Edit an event then try an retrieve it from the DB
    """
    def test_edit_events(self):
        register_and_login()
        add_event()
        resp = c.post(reverse('socshare:edit_event',kwargs={"event_slug":slugify(valid_event["name"])}),copy_modify(valid_event,"description","CANCELLED DUE TO COVID-19"))
        self.assertTrue(resp.context == None,"")

    """
    Test the events page's ability to render events
    - This test relies on the valid_event having a description shorter than 200 characters other wise it will fail due to the concatinated version that is displayed
    """
    def test_events_page(self):
        register_and_login()
        add_event()
        resp = c.get(reverse('socshare:events'))
        suc,k = are_all_elements_present(resp.content,valid_event,{"date":0,"time":0,"location":0,"url":0})
        self.assertTrue(suc,f"Some info about the event is not shown : {k}")

    """
    Tests the page for an individual event
    """
    def test_event_page(self):
        register_and_login()
        add_event()
        resp = c.get(reverse('socshare:event',kwargs={"event_slug":slugify(valid_event["name"])}))
        suc,k = are_all_elements_present(resp.content,valid_event,{"date":0,"time":0,"location":0})
        self.assertTrue(suc,f"Some info about the event is not shown : {k}")

    """
    Remove an event then try an retrieve it from the DB
    """
    def test_create_events_fuzz(self):
        register_and_login()
        add_event()
        suc,k = nulls_fuzzer(reverse('socshare:add_event'),valid_event,required_mask={"url":0})
        self.assertTrue(suc,f"The first field to inccorrectly accept a null was {k}")

    """
    Remove an event then try an retrieve it from the DB
    """
    def test_remove_events(self):
        register_and_login()
        add_event()
        resp = c.get(reverse('socshare:remove_event',kwargs={"event_slug":slugify(valid_event["name"])}))
        self.assertTrue(resp.url == "/dashboard/")
        
        resp = c.get(reverse('socshare:event',kwargs={"event_slug":slugify(valid_event["name"])}))
        self.assertFalse(valid_event["name"] in str(resp.content))
