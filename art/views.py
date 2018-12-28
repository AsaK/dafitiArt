# Create your views here.
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from art.forms import ArtRequestForm
from art.models import ArtRequest


class ArtRequestList(ListView):
    template_name = 'art/art_request_list.html'
    model = ArtRequest
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(ArtRequestList, self).get_context_data()
        context['page_title'] = 'DafitiArt | Art Request List'
        return context


class ArtRequestCreate(CreateView):
    model = ArtRequest
    form_class = ArtRequestForm
    template_name = 'art/art_request_form.html'
    success_url = reverse_lazy('art_request.list')

    def form_valid(self, form):
        response = super(ArtRequestCreate, self).form_valid(form)
        form.insert_events()
        messages.add_message(self.request, messages.SUCCESS, 'New request entered into the system')
        return response

    def get_context_data(self, **kwargs):
        context = super(ArtRequestCreate, self).get_context_data()
        context['page_title'] = 'DafitiArt | Create Art Request'
        return context
