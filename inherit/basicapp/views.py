from django.shortcuts import render
from .forms import UserProfileInfoForm, UserInfoForm

from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate

# Create your views here.

def index(request):
    return render(request, 'basicapp/index.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def user_login(request):

    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('User has not been activated')
        else:
            return HttpResponse('Login Failed!')
            print('Failed login attempt')
            print('Username:{} Password:{}'.format(username,password))
    else:
        return render(request, 'basicapp/login.html')


def register(request):

    registered = False

    if request.method == 'POST':
        user_form = UserInfoForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'prof_pic' in request.FILES:
                profile.prof_pic = request.FILES['prof_pic']
            profile.save()

            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserInfoForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'basicapp/register.html',
                              {'registered':registered, 'user_form':user_form,
                                'profile_form':profile_form, })
