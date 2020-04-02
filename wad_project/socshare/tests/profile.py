from socshare.tests.tests_core import *

"""
Testing the Profile Page
"""
class Profile(TestCase):
    """
    Test the profiles page's ability to render profiles for each society
    """
    def test_profiles_page(self):
        register_and_login()
        resp = c.get(reverse('socshare:profiles'))
        suc,k = are_all_elements_present(resp.content,valid_profile)
        self.assertTrue(suc,f"Some info about the profile is not shown : {k}")

    """
    Test the profiles page's ability to render profiles for each society
    """
    def test_profile_page(self):
        register_and_login()
        resp = c.get(reverse('socshare:profile',kwargs={"profile_slug":valid_profile["slug"]}))
        suc,k = are_all_elements_present(resp.content,valid_profile,{"slug":0})
        self.assertTrue(suc,f"Some info about the profile is not shown : {k}")

    """
    Test the profiles page's ability to render profiles for each society
    """
    def test_user_profile_page(self):
        register_and_login()
        resp = c.get(reverse('socshare:user_profile'))
        suc,k = are_all_elements_present(resp.content,valid_profile,{"slug":0})
        self.assertTrue(suc,f"Some info about the profile is not shown : {k}")