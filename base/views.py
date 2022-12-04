from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, FormView, CreateView

from base.forms import RoomForm
from base.models import Room, Message

# Create your views here.


def hello(request):
    s = request.GET.get("s", "")
    return HttpResponse(f"Hello {s}!")


# def rooms(request):
#     rooms = Room.objects.all()  # získání názvu všech místností
#     context = {'rooms': rooms}  # přidání vazby na html soubor (ve for loopě je 'rooms')
#     return render(request, template_name='base/rooms.html', context=context)  # renderování stránky


# class based view - využívá parent classu, abychom neuseli psát tolik kódu - o return a proměnnou méně než v
# zakomentovaném kódu nahoře
#Je ale potřeba v URL přepsat cestu na ....RoomsView.as_view()
# class RoomsView(TemplateView):
#     template_name = 'base/rooms.html'
#     extra_context = {'rooms': Room.objects.all()}

#Děděním z ListView není možné filtrovat výsledky!!! Jde o základní nejjednodušší třídní view
#Vrací kontext object_list, proto je ptořeba v HTML souboru toto přepsat
class RoomsView(ListView):
    template_name = 'base/rooms.html'
    model = Room


def room(request, id):
    room = Room.objects.get(id=id)  # získání místnosti podle id
    messages = room.message_set.all()  # vybrání všech zpráv v dané místnosti
    context = {'messages': messages, 'room': room}  # předání proměnných pro HTML soubor
    return render(request, template_name='base/room.html', context=context)  # render webovky

# Tato třída je ta samá jako ta s Create view, jen je delší zápis
# class RoomCreateView(FormView):
#     template_name = 'base/room_form.html'
#     form_class = RoomForm
#     success_url = reverse_lazy('rooms')
#
#     def form_valid(self, form):
#         cleaned_data = form.cleaned_data
#         Room.objects.create(
#             name=cleaned_data['name'],
#             description=cleaned_data['description']
#         )
#         return super().form_valid(form)

# Stejné jako nahoře, jen je potřeba do form.py přidat třídu Meta


class RoomCreateView(CreateView):
    template_name = 'base/room_form.html'
    form_class = RoomForm
    success_url = reverse_lazy('rooms')