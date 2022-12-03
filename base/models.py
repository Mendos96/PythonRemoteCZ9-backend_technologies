from django.contrib.auth.models import User
from django.db import models
from django.db.models import Model

# Create your models here.


class Room(Model):
    name = models.CharField(max_length=200, unique=True)  # Zadáváme název místnosti
    description = models.TextField(null=True, blank=True)  # Umožníme zadání popisku místnosti - může být prázdný (null) nebo i jen whitespaces (blank)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)  # Přidání uživatelů účastnících se konverzace v místnosti - vztah Many to Many
    created = models.DateTimeField(auto_now_add=True)  #Přidání času vytvoření místnosti
    updated = models.DateTimeField(auto_now=True)  #Přidání času modifikace místnosti

    def __str__(self):  # Formátování, jak se má zobrazit class jako string
        return self.name

    class Meta:
        ordering = ['-created', 'name']  # Seřazení místností podle data vytvoření (pomocí - od nejnovějšího po nejstarší), pokud by byly stejné tak podle jména

class Message(Model):
    body = models.TextField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.body[0:50]

    class Meta:
        ordering = ['-created', 'body']
