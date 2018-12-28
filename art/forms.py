from django import forms

from art.choices import STATUS_CHOICES
from art.models import ArtRequest, ArtRequestEvent


class ArtRequestForm(forms.ModelForm):
    status = forms.ChoiceField(STATUS_CHOICES, initial=1)
    progress = forms.FloatField(max_value=100, min_value=0, required=False)

    class Meta:
        model = ArtRequest
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ArtRequestForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs = {'class': 'form-control', 'placeholder': 'Name'}
        self.fields['description'].widget.attrs = {'class': 'form-control', 'placeholder': 'Description'}
        self.fields['owner'].widget.attrs = {'class': 'form-control', 'placeholder': 'Owner'}
        self.fields['owner'].help_text = 'Design that will be associated with the requisition   '
        self.fields['status'].widget.attrs = {'class': 'form-control', 'placeholder': 'Status'}
        self.fields['progress'].widget.attrs = {'class': 'form-control', 'placeholder': 'Progress'}

    def insert_events(self):
        if 'status' in self.cleaned_data:
            event_data = {
                'event_name': 'ChangeRequestStatus',
                'status': self.cleaned_data['status']
            }
            ArtRequestEvent.insert_art_event(self.instance.id, event_data)
        if 'progress' in self.cleaned_data:
            event_data = {
                'event_name': 'ChangeRequestProgress',
                'status': self.cleaned_data['progress']
            }
            ArtRequestEvent.insert_art_event(self.instance.id, event_data)
