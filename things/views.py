from django.core.context_processors import csrf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string

from .forms import ThingForm
from .models import Taker, Thing


THINGS_ON_PAGE = 50


def thing_list(request, token):
    things = Thing.objects.filter(Q(taken_by__token=token) |
                                  Q(taken_by__token__isnull=True))
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
