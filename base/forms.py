from logging import getLogger

from django import forms
from django.core.exceptions import ValidationError
from django.forms import Form, Textarea, ModelForm
from base.models import Room

# Třida určená pro View s děděním od FormView
# class RoomForm(Form):
#     name = forms.CharField(max_length=200)
#     description = forms.CharField(widget=Textarea, required=False)

# Třída určená pro View s děděním od CreateView

LOGGER = getLogger()


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['participants']

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 2:
            validation_error = "Name should contain at least 2 characters"
            LOGGER.warning(f'{validation_error}: {name}')
            raise ValidationError(validation_error)
        return name
