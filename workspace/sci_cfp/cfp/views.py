# -*- coding: utf-8 -*-

from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.db import IntegrityError
from django.utils import timezone

from cfp.models import *
from decorators import ajax_login_required


def index(request):
    events = Event.objects.all()
    favorites = Favorite.objects.filter(user_id=request.user.id)
    favorites = [f.event_id for f in favorites]
    paginator = Paginator(events, 10)

    try:
        page_number = int(request.GET.get('page', '1'))
    except ValueError:
        page_number = 1

    try:
        events = paginator.page(page_number)
    except (InvalidPage, EmptyPage):
        events = paginator.page(paginator.num_pages)

    return render(request, 'cfp/index.html', dict(events=events, favorites=favorites))


@csrf_protect
def login_user(request):
    if request.method == 'GET':
        next = request.GET.get('next', '')
        return render(request, 'cfp/login.html', dict(next=next))

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
        tags = request.POST.getlist('tags[]', '')

        try:
            user = User.objects.create_user(username=email, email=email, password=password, first_name=first_name, last_login=timezone.now())
            user.is_active = True
            user.save()

            for tag_id in tags:
                interest = Interest()
                interest.user_id = user.id
                interest.category_id = int(tag_id)
                interest.save()

        except IntegrityError:
            error = "Email address already registered."
            return render(request, "cfp/signup.html", dict(signup_error=error))

        return render(request, "cfp/confirmation.html", dict(type='signup'))
    else:
        return render(request, 'cfp/login.html', dict())


def search(request):
    if request.method == 'GET':

        paramQ = request.GET.get('q', '')
        
        events = Event.objects(__raw__= { '$or': [{'title_event': {'$regex': paramQ, '$options' : 'i'}}, 
        {'city': {'$regex': paramQ, '$options' : 'i'}},
        {'country': {'$regex': paramQ, '$options' : 'i'}},
        {'description': {'$regex': paramQ, '$options' : 'i'}},
        {'categories': {'$regex': paramQ, '$options' : 'i'}}]})
        paginator = Paginator(events, 10)
        try:
            page_number = int(request.GET.get('page', '1'))
        except ValueError:
            page_number = 1
        
        try:
            events = paginator.page(page_number)
        except (InvalidPage, EmptyPage):
            events = paginator.page(paginator.num_pages)
        
        return render(request, "cfp/search.html", {
            "events": events
        })
    else:
        return render(request, 'cfp/login.html', dict())


def event(request, event_id):
    user_id = request.user.id
    event = Event.objects.get(id=event_id)

    try:
        favorite = Favorite.objects.get(id=str(user_id) + event_id)
        followers = Favorite.objects.filter(event_id=event_id).count()
    except Favorite.DoesNotExist:
        favorite = None
        followers = 0
    try:
        reviews = Review.objects.filter(event_id=event_id)
        num_reviews = reviews.count()
    except Review.DoesNotExist:
        reviews = []
        num_reviews = 0

    stars = [r.stars for r in reviews]
    avg_stars = float(sum(stars))/len(stars) if len(stars) > 0 else 0
    num_stars = (15 + (avg_stars * len(stars))) / (5 + len(stars)) if len(stars) > 0 else 0

    paginator = Paginator(reviews, 5)
    reviews = paginator.page(1)
    return render(request, 'cfp/event.html', dict(event=event, favorite=favorite, num_followers=followers,
                                                  reviews=reviews, num_reviews=num_reviews, num_stars=num_stars,
                                                  has_next=reviews.has_next()))


@ajax_login_required
def event_review(request):
    if request.method == 'GET':
        raise Http404

    status = 200
    event_id = request.POST.get('e')
    stars = request.POST.get('s')
    text = request.POST.get('r')
    user_id = request.user.id

    review = Review()
    review.event_id = event_id
    review.user_id = user_id
    review.user_name = request.user.first_name
    review.stars = stars
    review.text = text
    review.date = timezone.now()
    review.save()

    return JsonResponse({'status': status})


def review(request):
    if request.method == 'POST':
        raise Http404

    num_page = request.GET.get('p')
    event_id = request.GET.get('e')
    num_ignore = request.GET.get('i')

    reviews = Review.objects.filter(event_id=event_id)
    paginator = Paginator(reviews[int(num_ignore):], 5)
    reviews = paginator.page(int(num_page))

    return render(request, 'cfp/embed_reviews.html', dict(reviews=reviews, num_page=num_page, has_next=reviews.has_next()))


@ajax_login_required
def favorite(request):
    if request.method == 'GET':
        raise Http404

    status = 200
    event_id = request.POST.get('d')
    save = request.POST.get('s')
    user_id = request.user.id

    if save == '1':
        favorite = Favorite()
        favorite.id = str(user_id) + event_id
        favorite.event_id = event_id
        favorite.user_id = user_id
        favorite.save()
    elif save == '0':
        Favorite.objects(id=str(user_id) + event_id).delete()
    else:
        status = 201

    followers = Favorite.objects.filter(event_id=event_id).count()

    return JsonResponse({'status': status, 'num_followers': followers})


@ajax_login_required
def notification_active(request):
    if request.method == 'GET':
        raise Http404

    status = 200
    event_id = request.POST.get('d')
    activate = request.POST.get('s')
    user_id = request.user.id
    favorite_id = str(user_id) + event_id

    favorite = Favorite.objects.get(id=favorite_id)

    if activate == 'true':
        favorite.notify = 1
    elif activate == 'false':
        favorite.notify = 0
    else:
        status = 201

    favorite.save()
    return JsonResponse({'status': status})


def get_categories(request):
    if request.method == 'GET':
        raise Http404

    data = [c.as_json() for c in Category.objects.all()]
    return JsonResponse({'categories': data})


@login_required(login_url='/cfp/login')
def profile(request):
    if request.method == 'GET':
        interests = [i.category_id for i in Interest.objects.filter(user_id=request.user.id)]
        return render(request, 'cfp/profile.html', dict(interests=interests))

    elif request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        email = request.POST.get('email', '').lower()
        tags = request.POST.getlist('tags[]', '')
        tags = [int(t) for t in tags]

        try:
            user = User.objects.get(id=request.user.id)
            user.first_name = first_name
            user.email = email
            user.save()

            Interest.objects.filter(user_id=request.user.id).delete()
            for tag_id in tags:
                interest = Interest()
                interest.user_id = request.user.id
                interest.category_id = tag_id
                interest.save()

        except IntegrityError:
            error = "Email address already exits."
            return render(request, "cfp/profile.html", dict(profile_error=error))

        return render(request, "cfp/profile.html", dict(interests=tags))