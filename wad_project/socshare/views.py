from django.shortcuts import render
from socshare.forms import UserForm, SocietyForm
from socshare.models import Society, Event, Comment
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.shortcuts import redirect
from socshare.utils.src import check_email
from django.template.defaultfilters import slugify

def events(request):
    search = request.GET.get('search')
    events = Event.objects.filter(name__icontains=search) if search else Event.objects.order_by('date')
    context = {"title":"Events","events":[x for x in events]}
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
                    print('Logged in to '+user.society.name)
                    return redirect(reverse('socshare:events'))
            else:
                print('Password wrong')
        else:
            print('Email does not exist')

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
            if check_email(email):
                username = slugify(name)
                user = User.objects.get_or_create(username=username)[0]
                user.email = email
                user.set_password(password)
                user.save()
                society = Society.objects.get_or_create(name=name, user=user)[0]
                society.acronym = acronym
                society.save()
                print('Successfully created user')
                login(request, user)
                return redirect(reverse('socshare:events'))
            else:
                print('Society not found on SRC')
        else:
            print('Password doesn\'t match')
        
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