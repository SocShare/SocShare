from django.shortcuts import render
from socshare.forms import UserForm, SocietyForm
from socshare.models import Society, Event, Comment
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.shortcuts import redirect
from socshare.utils.src import check_email
from django.template.defaultfilters import slugify
from django.db.models.functions.datetime import datetime
from django.conf import settings

def events(request):
    search = request.GET.get('search')
    events = Event.objects.filter(name__icontains=search) if search else Event.objects.order_by('date')
    context = {"title":"Events","events":[x for x in events]}
    if search:
        context['search']=search
    return render(request,'socshare/events.html',context=context)

def calendar(request):
    return render(request,'socshare/calendar.html')

def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(email=email).count()>=1:
            user = authenticate(username=User.objects.get(email=email).username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse('socshare:events'))
        return render(request,'socshare/login.html',context={'alert':'danger','alert_msg':'Email/password is incorrect!'})

    return render(request,'socshare/login.html',context={"title":"Login"})

def logout_page(request):
    logout(request)
    return redirect(reverse('socshare:events'))

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        verify = request.POST.get('verify')
        name = request.POST.get('name')
        acronym = request.POST.get('acronym')
        if password == verify:
            if settings.PROD:
                if User.objects.filter(email=email).count()!=0:
                    return render(request,'socshare/register.html',context={'alert':'warning','alert_msg':'An account is already registered with this email address!'})
                if Society.objects.filter(acronym=acronym).count()!=0:
                    return render(request,'socshare/register.html',context={'alert':'warning','alert_msg':'Another society already has this acronym!'})
                username = slugify(name)
                user = User.objects.get_or_create(username=username)[0]
                user.email = email
                user.set_password(password)
                user.save()
                society = Society.objects.get_or_create(name=name, user=user)[0]
                society.acronym = acronym
                society.save()
                login(request, user)
                return redirect(reverse('socshare:events'))
            else:
                if check_email(email):
                    if User.objects.filter(email=email).count()!=0:
                        return render(request,'socshare/register.html',context={'alert':'warning','alert_msg':'An account is already registered with this email address!'})
                    if Society.objects.filter(acronym=acronym).count()!=0:
                        return render(request,'socshare/register.html',context={'alert':'warning','alert_msg':'Another society already has this acronym!'})
                    username = slugify(name)
                    user = User.objects.get_or_create(username=username)[0]
                    user.email = email
                    user.set_password(password)
                    user.save()
                    society = Society.objects.get_or_create(name=name, user=user)[0]
                    society.acronym = acronym
                    society.save()
                    login(request, user)
                    return redirect(reverse('socshare:events'))
                else:
                    return render(request,'socshare/register.html',context={'alert':'warning','alert_msg':'Account not registered with SRC!'})
        else:
            return render(request,'socshare/register.html',context={'alert':'danger','alert_msg':'Passwords do not match!'})
    return render(request,'socshare/register.html')

def dashboard(request):
    if request.user.is_authenticated:
        events = Event.objects.filter(society=request.user.society)
        return render(request,'socshare/dashboard.html',context={'events':events})
    return redirect(reverse('socshare:events'))

def add_event(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            name=request.POST.get('name')
            date=request.POST.get('date')
            time=request.POST.get('time')
            location=request.POST.get('location')
            url=request.POST.get('url')
            description=request.POST.get('description')
            date=datetime.strptime(date+' '+time,'%Y-%m-%d %H:%M')
            event = Event.objects.get_or_create(name=name,society=request.user.society)[0]
            event.description=description
            event.date=date
            event.ticket_url=url
            event.society=request.user.society
            event.location=location
            banner=request.FILES.get('banner')
            if banner:
                event.banner=banner
            event.save()
            return redirect(reverse('socshare:dashboard'))
    return redirect(reverse('socshare:events'))

def remove_event(request,event_slug):
    if request.user.is_authenticated:
        event=Event.objects.filter(slug=event_slug)
        if event.count()>0:
            event=event[0]
            if request.user.society == event.society:
                event.delete()
        return redirect(reverse('socshare:dashboard'))
    return redirect(reverse('socshare:events'))

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

def user_profile(request):
    if request.user.is_authenticated:
        society = request.user.society
        context = {
            "title":society.acronym.upper()+" Profile",
            "name":society.name,
            "fullscreen":True, 
            "logo":society.profile,
            "banner_img_url":society.banner, 
            "events":Event.objects.filter(society=society)
        }
        return render(request,'socshare/profile.html',context=context)
    return redirect(reverse('socshare:login'))

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