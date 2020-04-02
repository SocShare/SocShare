from django.test import TestCase
from django.test import Client
from django.urls import reverse, resolve
from django.template.defaultfilters import slugify

# To check the SRC checks are functioning correctly
valid_email = "pausegaminglan@gmail.com"
non_valid_email = "example@example.co.uk"
valid_registration = {"email":valid_email,"password":'test',"verify":'test',"name":'This is a test',"acronym":'tiat'}
valid_profile = {"name":valid_registration["name"],"slug":valid_registration["acronym"]}
valid_login = {"email":valid_registration["email"],"username":slugify(valid_registration["name"]),"password":valid_registration["password"]}
valid_event = {"name":"Testing Everything","date":"2020-04-30","time":"20:02","location":"55.87159101963893, -4.28941011428833","url":"https://tsb.bz/r","description":"Because this is a test is now affiliated with the SRC we have decided to through a party where we test everything within the SRC site"}
c = Client()

def register_with_vaild():
    c.post(reverse('socshare:register'),valid_registration)

def register_and_login():
    register_with_vaild()
    login_with_vaild()

def login_with_vaild():
    return c.login(username=slugify(valid_registration["name"]),password=valid_registration["password"])

def add_event():
    c.post(reverse('socshare:add_event'),valid_event)

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

def are_all_elements_present(s,dic,mask=None):
    for k in dic:
        if dic[k] not in str(s):
            if mask != None:
                if mask.get(k,1) == 1:
                    return False,k
            else:
                return False,k
                
    return True,""