from django.shortcuts import render, redirect
from .forms import RegisterWriterForm, WriterProfileForm
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from .models import User
import json


# Create your views here.
def home(request, template="accounts/home.html"):
    page_title = 'Home'
    return render(request, template, locals())


@csrf_exempt
def register(request, template="accounts/register.html"):
    if request.user.is_authenticated:
        return redirect('/accounts/home')
    register_form = RegisterWriterForm()
    profile_form = WriterProfileForm()
    if request.method == 'POST':
        postdata = request.POST.copy()
        postfiles = request.FILES.copy()
        register_form = RegisterWriterForm(postdata)
        profile_form = WriterProfileForm(postdata, postfiles)
        print(postdata)
        print(postfiles.get('certificate', 'non'))
        # list.replace("[", "").replace("]", "").replace("'", "").split(",")
        if register_form.is_valid() and profile_form.is_valid():
            user = register_form.save(commit=False)
            user.user_type = 'writer'
            user.set_password(register_form.cleaned_data['password2'])
            user.save()
            user1 = authenticate(request, username=user.username, password=postdata['password2'])
            login(request, user1)
            if authenticate(request, username=user.username, password=postdata['password2']):
                form = profile_form.save(commit=False)
                print(form)
                print(request.user)
                form.user = user
                form.save()
                path = request.GET.get('next', '')
                print(path + '  1test')
                if len(request.GET.get('next', '')) > 3:
                    path = request.GET.get('next', '')
                    print(path)
                    return redirect(path)
                return redirect('home')

            print("True Kabisa")
            pass
        else:
            error_message = 'Correct the errors below'
    page_title = 'Register'
    path = request.GET.get('next', '')
    return render(request, template, locals())


def login_view(request, template="accounts/login.html"):
    if request.method == 'POST':
        postdata = request.POST.copy()
        username = postdata['username']
        password = postdata['password']
        user = User.objects.filter(email=username)
        if user.count() == 1:
            username = user[0].username
        user1 = authenticate(request, username=username, password=password)
        if user1:
            login(request, user1)
            path = request.GET.get('next', '')
            if path:
                return redirect(path)
            return redirect('home')
        else:
            user_error = 'Invalid Username or Password'
    page_title = 'Login'
    path = request.GET.get('next', '')
    return render(request, template, locals())


def logout_view(request):
    logout(request)
    return redirect('home')
