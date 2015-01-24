from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render, redirect

from .models import Thing, Taker


def thing_list(request, token):
    things = Thing.objects.all()
    return render(request, 'things/list.html',
        {'things': things, 'token': token})


def thing_detail(request, token, pk):
    thing = get_object_or_404(Thing, pk=pk)
    return render(request, 'things/detail.html', 
        {'thing': thing, 'token': token})


def thing_take(request, token, pk):
    thing = get_object_or_404(Thing, pk=pk)
    taker_token = request.POST.get('taker_token')
    thing_taker = get_object_or_404(Taker, token=taker_token)
    if request.method == "POST":
        thing.give_to(thing_taker)
    return redirect(reverse('things:detail',
        kwargs={'pk': thing.pk, 'token': token}))


def thing_give_back(request, token, pk):
    thing = get_object_or_404(Thing, pk=pk)
    taker_token = request.POST.get('taker_token')
    thing_taker = get_object_or_404(Taker, token=taker_token)
    if request.method == "POST":
        thing.give_back(thing_taker)
    return redirect(reverse('things:detail',
        kwargs={'pk': thing.pk, 'token': token}))
