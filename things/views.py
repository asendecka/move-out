# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, Http404, render, redirect
from django.template.loader import render_to_string
from django.utils import timezone

from .forms import ThingForm
from .models import Taker, Thing


THINGS_ON_PAGE = 51


superuser_required = user_passes_test(lambda user: user.is_superuser)


def thing_list(request, token):
    things = Thing.objects.filter(Q(taken_by__token=token) |
                                  Q(taken_by__token__isnull=True)
                                  ).order_by('id')
    paginator = Paginator(things, THINGS_ON_PAGE)
    taker = get_object_or_404(Taker, token=token)

    page = request.GET.get('page')
    try:
        things = paginator.page(page)
    except PageNotAnInteger:
        things = paginator.page(1)
    except EmptyPage:
        things = paginator.page(paginator.num_pages)
    return render(request, 'things/list.html',
                  {'things': things, 'token': token, 'taker': taker})


def thing_detail(request, token, pk):
    thing = get_object_or_404(Thing, pk=pk)
    taker = get_object_or_404(Taker, token=token)
    return render(request, 'things/detail.html',
                  {'thing': thing, 'token': token, 'taker': taker})


def thing_take(request, token, pk):
    thing = get_object_or_404(Thing, pk=pk, taken_by=None)
    thing_taker = get_object_or_404(Taker, token=token)
    if request.method == "POST":
        is_ajax = request.POST.get('is_ajax')
        thing.give_to(thing_taker)
        if is_ajax:
            params = {'token': token, 'thing': thing, 'css_class': 'booking'}
            params.update(csrf(request))
            data = render_to_string('things/include/give_back_form.html',
                                    params)
            return JsonResponse({'msg': "Twoje!", 'form': data})
    return redirect('things:detail', pk=thing.pk, token=token)


def thing_give_back(request, token, pk):
    thing = get_object_or_404(Thing, pk=pk, taken_by__token=token)
    thing_taker = get_object_or_404(Taker, token=token)
    if request.method == "POST":
        is_ajax = request.POST.get('is_ajax')
        thing.give_back(thing_taker)
        if is_ajax:
            params = {'token': token, 'thing': thing, 'css_class': 'booking'}
            params.update(csrf(request))
            data = render_to_string('things/include/take_form.html',
                                    params)
            return JsonResponse({'msg': "Oddane!", 'form': data})
    return redirect(reverse('things:detail',
                    kwargs={'pk': thing.pk, 'token': token}))

@superuser_required
def thing_add(request, token):
    if request.method == "POST":
        form = ThingForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            if request.POST.get("save") == "Zapisz":
                return redirect(reverse('things:detail',
                                kwargs={'pk': instance.pk, 'token': token}))
            else:
                form = ThingForm()
    else:
        form = ThingForm()
    return render(request, 'things/add.html', {'token': token, 'form': form})


def taker_list(request, token):
    takers = Taker.objects.all()
    return render(request, 'things/taker_list.html',
                  {'takers': takers, 'token': token})

@superuser_required
def send_mail_to_taker(request, token, taker_pk):
    taker = get_object_or_404(Taker, pk=taker_pk)
    if not taker.email:
        return JsonResponse({'msg': "Brak e-maila", "error": True})
    subject = "Rozdajemy nasze rzeczy!"
    content = render_to_string('things/mail/taker_link.html',
        {'taker_token': taker.token, 'token': token})
    send_mail(subject, content, settings.SENDGRID_FROM_EMAIL, [taker.email])
    taker.email_sent = timezone.now()
    taker.save()
    return JsonResponse({'msg': " (Wysłane!) "})

def my_things(request, token):
    taker = get_object_or_404(Taker, token=token)
    things = Thing.objects.filter(taken_by=taker)
    paginator = Paginator(things, THINGS_ON_PAGE)
    taker = get_object_or_404(Taker, token=token)

    page = request.GET.get('page')
    try:
        things = paginator.page(page)
    except PageNotAnInteger:
        things = paginator.page(1)
    except EmptyPage:
        things = paginator.page(paginator.num_pages)
    return render(request, 'things/my_list.html',
                  {'things': things, 'token': token, 'taker': taker})

@superuser_required
def taker_things(request, token, taker_pk):
    taker = get_object_or_404(Taker, pk=taker_pk)
    things = taker.taken_things()
    paginator = Paginator(things, THINGS_ON_PAGE)
    
    page = request.GET.get('page')
    try:
        things = paginator.page(page)
    except PageNotAnInteger:
        things = paginator.page(1)
    except EmptyPage:
        things = paginator.page(paginator.num_pages)
    return render(request, 'things/taker_things.html',
                  {'things': things, 'token': token, 'taker': taker})

@superuser_required
def thing_gone(request, token, pk):
    assert request.method == "POST"
    thing = get_object_or_404(Thing, pk=pk)
    thing.is_gone()
    params = {'token': token, 'thing': thing, 'css_class': 'booking'}
    params.update(csrf(request))
    data = render_to_string('things/include/not_gone_form.html', params)
    return JsonResponse({'msg': "Zabrane", 'form': data})

@superuser_required
def thing_not_gone(request, token, pk):
    assert request.method == "POST"
    thing = get_object_or_404(Thing, pk=pk)
    thing.is_not_gone()
    params = {'token': token, 'thing': thing, 'css_class': 'booking'}
    params.update(csrf(request))
    data = render_to_string('things/include/gone_form.html', params)
    return JsonResponse({'msg': "Oddane", 'form': data})
