# To check the SRC checks are functioning correctly

# Vaild email: pausegaminglan@gmail.com
# Not Vaild Email: example@example.co.uk

from django.test import TestCase
from django.test import Client
from django.urls import reverse, resolve
from django.template.defaultfilters import slugify

vaild_email = "pausegaminglan@gmail.com"
non_vaild_email = "example@example.co.uk"

c = Client()

def nulls_fuzzer(url,valid_input,required_mask=None):
    for i,k in enumerate(valid_input):
        resp = c.post(url,)
        if resp.context != None and resp.context["alert_msg"] != None:
            if required_mask == None:
                return False
            elif required_mask[i] == 1:
                return False
    return True