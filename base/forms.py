from django import forms
from django.forms import Form, Textarea


class RoomForm(Form):
    name = forms.CharField(max_length=200)
    description = forms.CharField(widget=Textarea, required=False)
