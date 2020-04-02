import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','wad_project.settings')
import django
django.setup()
from socshare.models import Society, Event, Comment
from django.contrib.auth.models import User
import datetime

# Had to make the comments global due to some scope issues, sorry :c
comments = [
        {'content':'Nice event, very cool!'},
        {'content':'Awesome!'},
        {'content':'Disappointing event, lost my sister and was unable to find her for a solid 20 minutes...'},
        {'content':'I like this, thank you :D'},
        {'content':'Spent so long doing my WAD project that I completely forgot to go. Hope I didn\'t miss out on too much :('}
    ]

def populate():
    gusec = {'name':'Glasgow University Security Society',
        'acronym':'gusec',
        'profile':'profile/logo_blue.png',
        'banner':'profile_banner/matrix.png',
        'description':'''Welcome to the official page for Glasgow University Security Society (GUSEC). This will be our main method of communication with members, so if you want to stay updated on events and other workshops then make sure to check the Discord regularly!

If you wish to contact us you can DM a board member, join our discord server or send an email to our society email address: gusecsoc@gmail.com

You can follow us on social media @gusecurity on Instagram and Twitter.
        ''',
        'events':[{'name':'Hackerspace',
                'location':'55.873921, -4.291174',
                'ticket_url':'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                'description':'''
                Come along to our weekly hacking socials, anyone is welcome – even if you’ve never touched a computer before. A hackerspace is a place where you can work on your projects, chat with others, make new things and learn. 
There are no official workshops, lectures or talks going on (although we may have the occasional guest speaker in), so feel free to show up and do your own thing or we can give you some challenges and point you in the right direction. 
This is a great opportunity if you want to learn about cyber security in a chilled environment, so pop in any time and ask questions!

We'll be in the QMU CS study zone at 5:30.
                ''',
                'date':datetime.datetime(2020, 5, 17, 17, 30)
                }]
        }
    guts = {'name':'Glasgow University Tech Society',
            'acronym':'guts',
            'profile':'profile/guts.jpg',
            'banner':'profile_banner/matrix.png',
            'description':'''GUTS is a student society of hackers. We love everything to do with technology, so we host as many events as we can to bring students closer to the topics that excite them (from human centred security all the way down to the bits and bytes). Our annual hackathon and Cyber Defence Execsie events will give you the opportunity to unleash your creativity and chat to loads of industry experts, so why not come along?
            ''',
            'events':[{'name':'Hackathon',
                    'description':'''The annual biggest tech event in town is back once again, hosted by the Glasgow University Tech Society! Held in collaboration with the School of Computing Science and influential tech companies based in the UK. This is your chance to show your coding ability, nudge your foot in the industry door or just have fun and eat free pizza!

The event is open to all students and no previous coding experience is required! If you don't have a team, don’t worry, you can arrange one on the spot! Food and drink are provided to make sure you are at your best the entire way through. 

It all begins with choosing from some of the great challenges that you and your team will take on. The event runs the entire weekend, and while sleeping is optional, sleeping spaces are provided, but remember to bring a sleeping bag!

The event is entirely free, however tickets and places are limited, so grab yours as soon as you can! We hope you join us on this coding adventure!

The first batch of tickets will go live at 19th of September, 1700.

For further information and a peek at our previous hacks,visit gutechsoc.com/hackathon.
                    ''',
                    'location':'55.873935, -4.292079',
                    'date':datetime.datetime(2020, 9, 30, 9)
                    },
                    {'name':'Hacker Olympics',
                    'description':'''Glasgow University's Hacker Olympics is a one-day event where teams of students compete to solve as many challenges as they can in order to earn points. The team with the highest number of points at the end wins!

If you don't have a team beforehand, you can come along and form one with the people you meet on the day! 

And don't worry if you’re not an elite programmer either - there are challenges for students of all levels, and some challenges are not related to programming at all! All you need is a laptop. 

Come for an opportunity to make friends, solve interesting challenges, and, most importantly, get free pizza for lunch!
                    ''',
                    'date':datetime.datetime(2020, 10, 12, 9)
                    }]
            }
    bms = {'name':'Bad Movie Society',
            'acronym':'bms',
            'banner':'profile_banner/Bad-Movie.png',
            'description':'''The Bad Movie Society is a cult set up for the consumption, appreciation and dissemination of the worst that cinema has to offer. We screen B-movies of every genre and welcome all enthusiasts. Dress code is casual, popcorn is salted.
            ''',
            'events':[{'name':'Bad Movie Night',
                    'description':'''
                    Cool 80's music, a high profile cast and even a recent Netflix adaptation, so it's in the wrong society? Not quite, some consider it to be one of the worst movies ever (luckily)! If you embrace the film's silliness, you are going to enjoy it though, so come by with your friends, entry is as always free
                    ''',
                    'date':datetime.datetime(2020, 4, 12, 18)
                    }]
            }
    users = [
        {'username':'gusec',
        'email':'gusecurity@protonmail.com',
        'society':gusec},
        {'username':'guts',
        'email':'gutechsoc@gmail.com',
        'society':guts},
        {'username':'badmovies',
        'email':'gubadmoviesoc@gmail.com',
        'society':bms}
    ]

    users = [add_user(x['username'],x['email'],x['society']) for x in users]


def add_user(name,email,society=None):
    '''
    Helper function to setup a user with a default password
    '''
    user = User.objects.get_or_create(username=name)[0]
    user.email = email
    user.set_password('password')
    user.save()
    if society:
        add_society(society['name'],society['acronym'],society['events'],user,profile=society.get('profile'),banner=society.get('banner'),desc=society.get('description'))
    return user

def add_society(name,acronym,events,user, ticket_url=None,profile=None,banner=None,desc=None):
    '''
    Helper function to setup a society
    '''
    society = Society.objects.get_or_create(name=name, user=user)[0]
    society.acronym = acronym
    if desc: society.description = desc
    if profile: society.profile = profile 
    if banner: society.banner = banner
    society.save()
    events = [add_event(x['name'],x['description'],x['date'],society,banner=x.get('banner'),location=x.get('location'), ticket_url = x.get('ticket_url')) for x in events]
    return society

def add_event(name,description,date,society,ticket_url = None, banner=None,location=None):
    '''
    Helper function to setup an event
    '''
    event = Event.objects.get_or_create(name=name,society=society)[0]
    event.description = description
    event.date = date
    if ticket_url: event.ticket_url = ticket_url
    if banner: event.banner = banner
    if location: event.location = location
    event.save()
    for comment in comments:
        add_comment(comment['content'],event)
    return event

def add_comment(content, event):
    '''
    Helper function to setup a comment
    '''
    comment = Comment.objects.get_or_create(content=content, event=event)[0]
    # Fake Google Auth token for testing
    comment.auth='test_token'
    comment.save()
    return comment

if __name__ == '__main__':
    print('Populating database...')
    populate()
    print('Database has been populated :) \nIgnore any datetime warnings as we are using fixed times for testing, so don\'t need to be conerned about timezones.')