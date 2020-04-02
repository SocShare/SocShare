from socshare.tests.tests_core import *

"""
Testing the Profile Page
"""
class Profile(TestCase):
    """
    Test the events page's ability to render events
    - This test relies on the valid_event having a description shorter than 200 characters other wise it will fail due to the concatinated version that is displayed
    """
    def test_dashboard_events_rendering(self):
        register_and_login()
        add_event()
        resp = c.get(reverse('socshare:dashboard'))
        suc,k = are_all_elements_present(resp.content,valid_event,{"date":0,"time":0,"location":0,"url":0})
        self.assertTrue(suc,f"Some info about the event is not shown : {k}")
