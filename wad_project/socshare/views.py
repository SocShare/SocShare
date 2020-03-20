from django.shortcuts import render

def events(request):
    context = {"pageTitle":"Events","events":[]}
    temp = {
                "name":"Card Title",
                "description":"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum sem risus, suscipit et commodo sed, viverra nec erat. Donec at tellus nec massa elementum posuere ac et turpis. Aliquam tristique lectus at congue fringilla. Donec et nibh eu leo gravida molestie.",
                "img":"test.png",
                "url":"Test"
            }
    for i in range(10):
        context["events"].append(temp)
    return render(request,'socshare/events.html',context=context)

def calendar(request):
    return render(request,'socshare/calendar.html')

def login(request):
    return render(request,'socshare/login.html')

def register(request):
    return render(request,'socshare/register.html')

def dashboard(request):
    return render(request,'socshare/dashboard.html')

def profile(request,profile_slug):
    context = {"pageTitle":"Events","banner_img_url":"test.png"}
    return render(request,'socshare/profile.html',context=context)

def event_page(request,event_slug):
    return render(request,'socshare/event.html')