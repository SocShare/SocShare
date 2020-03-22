from django.urls import path
from socshare import views

app_name = 'socshare'

urlpatterns = [
    path('', views.events, name='events'),
    path('test', views.test, name='test')
]