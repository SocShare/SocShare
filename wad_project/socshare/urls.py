from django.conf.urls import url
from django.urls import path
from socshare import views

app_name = 'socshare'

urlpatterns = [
    path('', views.events, name='index'),
    path('events/', views.events, name='events'),
    path('events/<slug:event_slug>', views.event_page, name='event_page'),
    path('calendar/', views.calendar, name='calendar'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/<slug:profile_slug>', views.profile, name='profile'),
]