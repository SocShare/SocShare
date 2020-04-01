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