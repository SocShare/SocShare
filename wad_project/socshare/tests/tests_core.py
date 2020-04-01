# To check the SRC checks are functioning correctly

# Vaild email: pausegaminglan@gmail.com
# Not Vaild Email: example@example.co.uk

from django.test import TestCase
from django.test import Client
from django.urls import reverse, resolve
from django.template.defaultfilters import slugify

valid_email = "pausegaminglan@gmail.com"
non_valid_email = "example@example.co.uk"
valid_registration = {"email":valid_email,"password":'test',"verify":'test',"name":'This is a test',"acronym":'tiat'}
valid_login = {"email":valid_registration["email"],"username":slugify(valid_registration["name"]),"password":valid_registration["password"]}
c = Client()

def login_with_vaild():
    return c.login(username=slugify(valid_registration["name"]),password=valid_registration["password"])

def fuzzer(url,valid_input,replacement,required_mask=None):
    for i,k in enumerate(valid_input):
        test_input = copy_modify(valid_input,k,replacement)
        resp = c.post(url,test_input)
        if not (resp.context != None and resp.context["alert_msg"] != None):
            if required_mask == None:
                return False,k
            elif required_mask[i] == 1:
                return False,k
    return True,None

def nulls_fuzzer(url,valid_input,required_mask=None):
    return fuzzer(url,valid_input,"",required_mask)

def copy_modify(dic,k,v=""):
    out = dic.copy()
    out[k] = v
    return out