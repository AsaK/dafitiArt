# Create your views here.
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, TemplateView

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
        form.instance.owner_id = self.request.user.id
        response = super(ArtRequestCreate, self).form_valid(form)
        form.events_handler(self.request)
        messages.add_message(self.request, messages.SUCCESS, 'New request entered into the system')
        return response

    def get_context_data(self, **kwargs):
        context = super(ArtRequestCreate, self).get_context_data()
        context['page_title'] = 'DafitiArt | Create Art Request'
        return context


class ArtRequestUpdate(UpdateView):
    model = ArtRequest
    form_class = ArtRequestForm
    template_name = 'art/art_request_form.html'
    success_url = reverse_lazy('art_request.list')

    def form_valid(self, form):
        response = super(ArtRequestUpdate, self).form_valid(form)
        form.events_handler(self.request)
        messages.add_message(self.request, messages.SUCCESS, 'Successfully changed the request')
        return response

    def get_context_data(self, **kwargs):
        context = super(ArtRequestUpdate, self).get_context_data()
        context['page_title'] = 'DafitiArt | Update Art Request'
        return context


class ArtRequestDetail(TemplateView):
    template_name = 'art/art_request_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ArtRequestDetail, self).get_context_data()
        object_id = kwargs.get('pk')
        context['object'] = ArtRequest.objects.get(id=object_id)
        context['page_title'] = 'DafitiArt | Update Art Detail'
        return context
