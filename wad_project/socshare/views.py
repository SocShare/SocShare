from django.shortcuts import render
from socshare.forms import UserForm, SocietyForm

def events(request):
    return render(request,'socshare/events.html')

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