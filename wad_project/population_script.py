import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','wad_project.settings')
import django
django.setup()
from socshare.models import Society, Event, Comment
from django.contrib.auth.models import User
import datetime

comments = [
        {'content':'Nice event, very cool!'},
        {'content':'Awesome!'},
        {'content':'Disappointing event, lost my sister and was unable to find her for a solid 20 minutes...'},
        {'content':'I like this, thank you :D'},
        {'content':'I have a personal grudge against Ryan Murphy and therefore dislike this event'}
    ]

def populate():
    gusec = {'name':'Glasgow University Security Society',
        'acronym':'GUSEC',
        'profile':'logo_blue.png',
        'banner':'matrix.png',
        'events':[{'name':'Hackerspace',
                'description':'A place to learn hacking a chill!',
                'date':datetime.datetime(2020, 5, 17, 17, 30)
                }]
        }
    guts = {'name':'Glasgow University Tech Society',
            'acronym':'GUTS',
            'profile':'guts.jpg',
            'banner':'matrix.png',
            'events':[{'name':'Hackathon',
                    'description':'Make some awesome projects and win prizes!',
                    'date':datetime.datetime(2020, 9, 30, 9)
                    },
                    {'name':'Hacker Olympics',
                    'description':'Complete coding challenges to win prizes!',
                    'date':datetime.datetime(2020, 10, 12, 9)
                    }]
            }
    bms = {'name':'Bad Movie Society',
            'acronym':'BMS',
            'banner':'Bad-Movie.png',
            'events':[{'name':'Bad Movie Night',
                    'description':'Come watch bad movies with us :)',
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
    user = User.objects.get_or_create(username=name)[0]
    user.email = email
    user.set_password('password')
    user.save()
    if society:
        add_society(society['name'],society['acronym'],society['events'],user,profile=society.get('profile'),banner=society.get('banner'))
    return user

def add_society(name,acronym,events,user,profile=None,banner=None):
    society = Society.objects.get_or_create(name=name, user=user)[0]
    society.acronym = acronym
    society.profile = profile or 'default.jpg'
    society.banner = banner or 'test.png'
    society.save()
    events = [add_event(x['name'],x['description'],x['date'],society) for x in events]
    return society

def add_event(name,description,date,society):
    event = Event.objects.get_or_create(name=name,society=society)[0]
    event.description = description
    event.date = date
    event.save()
    for comment in comments:
        add_comment(comment['content'],event)
    return event

def add_comment(content, event):
    comment = Comment.objects.get_or_create(content=content, author=test_user, event=event)[0]
    comment.save()
    return comment

if __name__ == '__main__':
    # Setup a test user for comments
    test_user = {'username':'commenter',
                    'email':'commenter@gmail.com'}
    test_user = add_user(test_user['username'],test_user['email'])
    print('Populating database...')
    populate()