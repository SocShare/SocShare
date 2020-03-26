from django.shortcuts import render
from socshare.forms import UserForm, SocietyForm
from socshare.models import Society, Event, Comment

dummy_event = {
                "name":"Card Title",
                "description":"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum sem risus, suscipit et commodo sed, viverra nec erat. Donec at tellus nec massa elementum posuere ac et turpis. Aliquam tristique lectus at congue fringilla. Donec et nibh eu leo gravida molestie.",
                "img":"test.png",
                "url":"Test"
            }

def events(request):
    context = {"title":"Events","events":[]}
    for event in Event.objects.all():
        context["events"].append({
            'name':event.name,
            'description':event.description[:200],
            'img':'test.png',
            'url':event.slug
        })
    return render(request,'socshare/events.html',context=context)

def calendar(request):
    return render(request,'socshare/calendar.html')

def login(request):
    return render(request,'socshare/login.html',context={"title":"Login"})

def register(request):
    return render(request,'socshare/register.html')

def dashboard(request):
    return render(request,'socshare/dashboard.html')

def profile(request,profile_slug):
    society = Society.objects.get(slug=profile_slug)
    context = {
        "title":society.acronym.upper()+" Profile",
        "name":society.name,
        "fullscreen":True, 
        "logo":society.profile,
        "banner_img_url":society.banner, 
        "events":Event.objects.filter(society=society)}
    return render(request,'socshare/profile.html',context=context)

def event_page(request,event_slug):
    return render(request,'socshare/event.html')

def test(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = SocietyForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered=True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = SocietyForm()

    return render(request, 'socshare/test.html',
                context={'user_form':user_form,
                        'profile_form':profile_form,
                        'registered':registered})