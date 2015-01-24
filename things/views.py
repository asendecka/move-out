from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render, redirect

from .forms import ThingForm
from .models import Taker, Thing


THINGS_ON_PAGE = 50


def thing_list(request, token):
    things = Thing.objects.all()
    paginator = Paginator(things, THINGS_ON_PAGE)

    page = request.GET.get('page')
    try:
        things = paginator.page(page)
    except PageNotAnInteger:
        things = paginator.page(1)
    except EmptyPage:
        things = paginator.page(paginator.num_pages)
    return render(request, 'things/list.html',
        {'things': things, 'token': token})


def thing_detail(request, token, pk):
    thing = get_object_or_404(Thing, pk=pk)
    return render(request, 'things/detail.html', 
        {'thing': thing, 'token': token})


def thing_take(request, token, pk):
    thing = get_object_or_404(Thing, pk=pk, taken_by=None)
    taker_token = request.POST.get('taker_token')
    thing_taker = get_object_or_404(Taker, token=taker_token)
    if request.method == "POST":
        thing.give_to(thing_taker)
    return redirect(reverse('things:detail',
        kwargs={'pk': thing.pk, 'token': token}))


def thing_give_back(request, token, pk):
    thing = get_object_or_404(Thing, pk=pk, taken_by__token=token)
    taker_token = request.POST.get('taker_token')
    thing_taker = get_object_or_404(Taker, token=taker_token)
    if request.method == "POST":
        thing.give_back(thing_taker)
    return redirect(reverse('things:detail',
        kwargs={'pk': thing.pk, 'token': token}))


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
