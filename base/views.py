from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, FormView, CreateView, DeleteView, UpdateView

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


class RoomsView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    template_name = 'base/rooms.html'
    model = Room
    permission_required = ['base.view_room']


@login_required
@permission_required(['base.view_room', 'base.view_message'])
def room(request, pk):
    room = Room.objects.get(id=pk)  # získání místnosti podle id

    #POST
    if request.method == "POST":
        if request.user.has_perm('base.add_message'):
            Message.objects.create(
                user=request.user,
                room=room,
                body=request.POST.get('body')
            )
            room.participants.add(request.user)
            room.save()
        return redirect('room', pk=pk)

    #GET
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


class RoomCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    template_name = 'base/room_form.html'
    form_class = RoomForm
    extra_context = {'title': 'Create room'}
    success_url = reverse_lazy('rooms')
    permission_required = ['base.add_room']


class RoomUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name = 'base/room_form.html'
    form_class = RoomForm
    extra_context = {'title': 'Update room'}
    success_url = reverse_lazy('rooms')
    model = Room
    permission_required = ['base.change_room']


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class RoomDeleteView(StaffRequiredMixin, PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    template_name = 'base/room_confirm_delete.html'
    model = Room
    success_url = reverse_lazy('rooms')
    permission_required = 'base.delete_room'


def handler403(request, exception):
    return render(request, '403.html', status=403)

