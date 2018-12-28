from django import forms
import json
from art.choices import STATUS_CHOICES
from art.models import ArtRequest, ArtRequestEvent


class ArtRequestForm(forms.ModelForm):
    status = forms.ChoiceField(STATUS_CHOICES, initial=1)
    progress = forms.IntegerField(max_value=100, min_value=0, required=False)

    class Meta:
        model = ArtRequest
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ArtRequestForm, self).__init__(*args, **kwargs)
        self.fields.pop('owner')
        self.fields['name'].widget.attrs = {'class': 'form-control', 'placeholder': 'Name'}
        self.fields['description'].widget.attrs = {'class': 'form-control', 'placeholder': 'Description'}
        self.fields['status'].widget.attrs = {'class': 'form-control', 'placeholder': 'Status'}
        self.fields['progress'].widget.attrs = {'class': 'form-control', 'placeholder': 'Progress'}

    def events_handler(self, request):
        if self.cleaned_data['status'] and not self.__equals_status():
            event_data = {
                'event_name': 'ChangeRequestStatus',
                'status': self.cleaned_data['status'],
                'status_label': self.__get_status_label(),
                'user': {
                    'id': request.user.id,
                    'name': request.user.name
                }
            }
            ArtRequestEvent.insert_art_event(self.instance.id, event_data)
        if self.cleaned_data['progress'] and self.instance.progress != self.cleaned_data['progress']:
            event_data = {
                'event_name': 'ChangeRequestProgress',
                'progress': self.cleaned_data['progress'],
                'user': {
                    'id': request.user.id,
                    'name': request.user.name
                }
            }
            ArtRequestEvent.insert_art_event(self.instance.id, event_data)

    def __equals_status(self):
        return self.instance.status == dict(STATUS_CHOICES)[int(self.cleaned_data['status'])]

    def __get_status_label(self):
        return dict(STATUS_CHOICES)[int(self.cleaned_data['status'])]