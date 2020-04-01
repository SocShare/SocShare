from django.test import TestCase
from django.test import Client
from django.urls import reverse, resolve
from django.template.defaultfilters import slugify

# To check the SRC checks are functioning correctly
valid_email = "pausegaminglan@gmail.com"
non_valid_email = "example@example.co.uk"
valid_registration = {"email":valid_email,"password":'test',"verify":'test',"name":'This is a test',"acronym":'tiat'}
valid_login = {"email":valid_registration["email"],"username":slugify(valid_registration["name"]),"password":valid_registration["password"]}
valid_event = {"name":"Testing Everything","date":"2020-04-30","time":"20:02","location":"55.87159101963893, -4.28941011428833","url":"https://tsb.bz/r","description":"Because this is a test is now affiliated with the SRC we have decided to through a party where we test everything within the SRC site"}
c = Client()

def login_with_vaild():
    return c.login(username=slugify(valid_registration["name"]),password=valid_registration["password"])

def fuzzer(url,valid_input,replacement,required_mask=None):
    for k in valid_input:
        test_input = copy_modify(valid_input,k,replacement)
        resp = c.post(url,test_input)
        if not (resp.context != None and resp.context["alert_msg"] != None):
            if required_mask == None:
                return False,k
            elif required_mask.get(k,1) == 1:
                return False,k
    return True,""

def nulls_fuzzer(url,valid_input,required_mask=None):
    return fuzzer(url,valid_input,"",required_mask)

def copy_modify(dic,k,v=""):
    out = dic.copy()
    out[k] = v
    return out