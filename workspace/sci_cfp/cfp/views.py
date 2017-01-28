# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.utils import timezone

def index(request):
    return render(request, 'cfp/index.html', dict())


@csrf_protect
def login_user(request):
    if request.method == 'GET':
        return render(request, 'cfp/login.html', dict())

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        next = request.POST.get('next', '/')

        response_dict = dict()
        user = authenticate(username=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                #request.session.set_expiry(30)
                return HttpResponseRedirect(next)
            else:
                response_dict['login_error'] = "Account is not active!"
        else:
            response_dict['login_error'] = "Incorrect email or password!"

        response_dict['email'] = email
        return render(request, 'cfp/login.html', response_dict)


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


def signup_user(request):
    if request.method == 'GET':
        return render(request, "cfp/signup.html", dict())
    elif request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        # last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '').lower()
        password = request.POST.get('password', '')
        try:
            user = User.objects.create_user(username=email, email=email, password=password, first_name=first_name, last_login=timezone.now())
            user.is_active = True
            user.save()
        except IntegrityError:
            error = "Email address already registered."
            return render(request, "cfp/signup.html", dict(signup_error=error))

        return render(request, "cfp/confirmation.html", dict(type='signup'))
    else:
        return render(request, 'cfp/login.html', dict())