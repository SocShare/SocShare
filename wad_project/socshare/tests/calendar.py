from socshare.tests.tests_core import *

"""
Testing the Calendar Page
"""
class Calendar(TestCase):
    """
    Test the Calendar page's ability to render events
    """
    def test_calendar_page(self):
        register_and_login()
        add_event()
        resp = c.get(reverse('socshare:calendar'))
        suc,k = are_all_elements_present(resp.content,valid_event,{"date":0,"time":0,"location":0})
        self.assertTrue(suc,f"Some info about the event is not shown : {k}")