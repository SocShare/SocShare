from django.shortcuts import render

def events(request):
    context = {"events":[
        {
            "name":"Card Title",
            "description":"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum sem risus, suscipit et commodo sed, viverra nec erat. Donec at tellus nec massa elementum posuere ac et turpis. Aliquam tristique lectus at congue fringilla. Donec et nibh eu leo gravida molestie.",
            "img":"Test",
            "url":"Test"
        },
                {
            "name":"Card Title",
            "description":"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum sem risus, suscipit et commodo sed, viverra nec erat. Donec at tellus nec massa elementum posuere ac et turpis. Aliquam tristique lectus at congue fringilla. Donec et nibh eu leo gravida molestie.",
            "img":"Test",
            "url":"Test"
        },
                {
            "name":"Card Title",
            "description":"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum sem risus, suscipit et commodo sed, viverra nec erat. Donec at tellus nec massa elementum posuere ac et turpis. Aliquam tristique lectus at congue fringilla. Donec et nibh eu leo gravida molestie.",
            "img":"Test",
            "url":"Test"
        },
                {
            "name":"Card Title",
            "description":"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum sem risus, suscipit et commodo sed, viverra nec erat. Donec at tellus nec massa elementum posuere ac et turpis. Aliquam tristique lectus at congue fringilla. Donec et nibh eu leo gravida molestie.",
            "img":"Test",
            "url":"Test"
        },
                {
            "name":"Card Title",
            "description":"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum sem risus, suscipit et commodo sed, viverra nec erat. Donec at tellus nec massa elementum posuere ac et turpis. Aliquam tristique lectus at congue fringilla. Donec et nibh eu leo gravida molestie.",
            "img":"Test",
            "url":"Test"
        },
                {
            "name":"Card Title",
            "description":"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum sem risus, suscipit et commodo sed, viverra nec erat. Donec at tellus nec massa elementum posuere ac et turpis. Aliquam tristique lectus at congue fringilla. Donec et nibh eu leo gravida molestie.",
            "img":"Test",
            "url":"Test"
        }
    ]}
    return render(request,'socshare/events.html',context=context)

def calendar(request):
    return render(request,'socshare/events.html')

def login(request):
    return render(request,'socshare/events.html')

def register(request):
    return render(request,'socshare/events.html')

def dashboard(request):
    return render(request,'socshare/events.html')