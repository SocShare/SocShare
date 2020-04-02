from django.conf.urls import url
from django.urls import path
from socshare import views

app_name = 'socshare'

urlpatterns = [
    path('', views.events, name='index'),
    path('events/', views.events, name='events'),
    path('events/<slug:event_slug>', views.event_page, name='event'),
    path('calendar/', views.calendar, name='calendar'),
    path('login/', views.login_page, name='login'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/<slug:profile_slug>', views.profile, name='profile'),
    path('profile/', views.user_profile, name='user_profile'),
    path('logout/', views.logout_page, name='logout'),
    path('dashboard/add', views.add_event, name='add_event'),
    path('dashboard/edit/<slug:event_slug>', views.edit_event, name = 'edit_event'),
    path('dashboard/remove/<slug:event_slug>', views.remove_event, name='remove_event'),
    path('profiles/', views.profiles, name='profiles'),
    path('dashboard/update_profile', views.update_profile, name='update_profile'),
    path('dashboard/update_account', views.update_account, name='update_account')
]