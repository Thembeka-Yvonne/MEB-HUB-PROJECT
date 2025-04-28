from django import forms
from events.models import Event

class EventForms(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['description','image','date','location','admin_id']
