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
import socshare.utils.google_auth as gauth

def events(request):
    search = request.GET.get('search')
    events = Event.objects.filter(name__icontains=search) if search else Event.objects.order_by('date')
    context = {"title":"Events","searchbar":True,"events":[x for x in events]}
    if search:
        context['search']=search
    return render(request,'socshare/events.html',context=context)

def event_page(request, event_slug):
    event = Event.objects.filter(slug = event_slug).get()
    # Neat trick for getting comments associated with the event
    comments = event.comment_set.order_by('-date')
    context = {"title":"Events","fullscreen":True,"event": event,"comments":comments}
    if request.method=='POST':
        token = request.POST.get('token')
        comment = request.POST.get('comment')
        id = gauth.authenticate(token)
        # check user is logged in
        if id==None:
            context['alert']='danger'
            context['alert_msg']='Please login with your Google account to make a comment.'
        else:
            # check if user has already commented
            if event.comment_set.filter(auth=id).count()>=1:
                context['alert']='warning'
                context['alert_msg']='You have already made a comment.'
            else:
                comment = Comment.objects.get_or_create(content=comment, event=event)[0]
                comment.auth=id
                comment.save()
    return render(request,'socshare/event.html',context=context)

def edit_event(request, event_slug):
    event = Event.objects.filter(slug=event_slug).get()
    if request.method == 'POST':
        name=request.POST.get('name')
        date=request.POST.get('date')
        time=request.POST.get('time')
        location=request.POST.get('location')
        url=request.POST.get('url')
        description=request.POST.get('description')
        if date:
            date=datetime.strptime(date+' '+time,'%Y-%m-%d %H:%M')
            event.date=date
        if name:
            event.name=name
        if description:
            event.description=description
        if url:
            event.ticket_url=url
        if location:
            event.location=location
        banner=request.FILES.get('banner')
        if banner:
            event.update_banner(banner)
        event.save()
        return redirect(reverse('socshare:dashboard'))
    context = {"title":"Events","event": event}
    return render(request, 'socshare/edit_event.html', context)

def profiles(request):
    search = request.GET.get('search')
    societies = Society.objects.filter(name__icontains=search) if search else Society.objects.order_by('name')
    context = {"title": "Societies", "searchbar":True, "society" : [s for s in societies]}
    return render(request, 'socshare/society.html', context)

def calendar(request):
    events = Event.objects.order_by('date')
    context = {"title":"Calendar","events":[x for x in events]}
    return render(request,'socshare/calendar.html', context=context)

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
        acronym = request.POST.get('acronym').lower()
        if not all([email,password,verify,name,acronym]):
            return render(request,'socshare/register.html',context={'alert':'warning','alert_msg':'Please fill in all the fields!'})
        if password == verify:
            if settings.PROD or check_email(email):
                if User.objects.filter(email=email).count()!=0:
                    return render(request,'socshare/register.html',context={'alert':'warning','alert_msg':'An account is already registered with this email address!'})
                if Society.objects.filter(name=name).count()!=0:
                    return render(request,'socshare/register.html',context={'alert':'warning','alert_msg':'Another society already has this name!'})
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
        return render(request,'socshare/dashboard.html',context={"title":"Dashboard","events":events,'email':request.user.email})
    return redirect(reverse('socshare:events'))

def update_profile(request):
    if request.method=='POST':
        society=request.user.society
        banner=request.FILES.get('banner')
        profile=request.FILES.get('profile')
        description=request.POST.get('description')
        if banner:
            society.update_banner(banner)
        if profile:
            society.update_profile(profile)
        if description:
            society.description=description
    return redirect(reverse('socshare:dashboard'))

def update_account(request):
    if request.method=='POST':
        email=request.POST.get('description')
        old=request.POST.get('oldPassword')
        password=request.POST.get('password')
        password_verify=request.POST.get('passwordVerify')
        if email:
            if settings.PROD or check_email(email):
                request.user.email=email
        if old and password and password_verify:
            user = authenticate(username=request.user.username, password=old)
            if user:
                if password==password_verify:
                    user.set_password(password)
                    user.save()
                    # automatically log user back in
                    login(request, user)
    return redirect(reverse('socshare:dashboard'))

def add_event(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            name=request.POST.get('name')
            date=request.POST.get('date')
            time=request.POST.get('time')
            location=request.POST.get('location')
            url=request.POST.get('url')
            description=request.POST.get('description')
            if all([name,date,time,location,description]):
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
            events = Event.objects.filter(society=request.user.society)
            return render(request,'socshare/dashboard.html',context={"title":"Dashboard","events":events,'alert':'danger','alert_msg':'Enter all the required fields!'})
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