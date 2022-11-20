from django.http import HttpResponse
from django.shortcuts import render
from base.models import Room

# Create your views here.


def hello(request):
    s = request.GET.get("s", "")
    return HttpResponse(f"Hello {s}!")


def rooms(request):
    rooms = Room.objects.all()  # získání názvu všech místností
    context = {'rooms': rooms}  # přidání vazby na html soubor (ve for loopě je 'rooms')
    return render(request, template_name='base/rooms.html', context=context)  # renderování stránky
