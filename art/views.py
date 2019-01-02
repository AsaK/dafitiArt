# coding=utf-8
# Create your views here.
from django.contrib import messages
from django.db.models import Q, Max, Case, When, IntegerField
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, TemplateView

from art.forms import ArtRequestForm, ArtRequestFileForm
from art.models import ArtRequest, ArtRequestEvent, ArtRequestFile
from core.models import User
from art.choices import STATUS_CHOICES


class ArtRequestList(ListView):
    template_name = 'art/art_request_list.html'
    model = ArtRequest
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(ArtRequestList, self).get_context_data()
        context['page_title'] = 'DafitiArt | Art Request List'
        return context

    def get_queryset(self):
        queryset = super(ArtRequestList, self).get_queryset()
        if self.request.user.type == User.DESIGNER:
            queryset = queryset.filter(responsible=self.request.user)

        search = self.request.GET.get('search')
        if search:
            search = str(search)
            try:
                status_id = [item for item in STATUS_CHOICES if item[1].lower() == search.lower()][0][0]
                return queryset.filter(status=status_id)
            except Exception as E:
                """
                    Se estourar um exception nao foi encontrado na lista superior
                """
                queryset = queryset.filter(id=search) if search.isdigit() else queryset.filter(name__contains=search)
        return queryset


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
        context['page_title'] = 'DafitiArt | Detail Art Detail'
        return context


class ArtRequestFileList(ListView):
    template_name = 'art/art_request_file.html'
    model = ArtRequestFile

    def get_context_data(self, **kwargs):
        context = super(ArtRequestFileList, self).get_context_data()
        context['page_title'] = 'DafitiArt | Art Request Files'
        context['art_request_id'] = self.kwargs.get('pk')
        return context

    def get_queryset(self):
        art_request_id = self.kwargs.get('pk')
        return super(ArtRequestFileList, self).get_queryset().filter(art_request_id=art_request_id)


class ArtRequestFileCreate(CreateView):
    model = ArtRequestFile
    form_class = ArtRequestFileForm
    template_name = 'art/art_request_file_form.html'

    def form_valid(self, form):
        form.instance.owner_id = self.request.user.id
        form.instance.art_request_id = self.kwargs.get('pk')
        response = super(ArtRequestFileCreate, self).form_valid(form)
        ArtRequestEvent.insert_art_event(
            art_request_id=form.instance.art_request_id,
            event='UploadFile',
            value=form.instance.name,
            user=self.request.user
        )
        messages.add_message(self.request, messages.SUCCESS, 'New file uploaded to request')
        return response

    def get_context_data(self, **kwargs):
        context = super(ArtRequestFileCreate, self).get_context_data()
        context['page_title'] = 'DafitiArt | Create Art Request'
        context['art_request_id'] = self.kwargs.get('pk')
        return context
    
    def form_invalid(self, form):
        return super(ArtRequestFileCreate, self).form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('art_request.files', kwargs={'pk': self.kwargs.get('pk')})


def load_designers(request):
    """
        Função que retorna todos os designers da aplicação.
    :param request:
    :return Json com todos os designers:
    """
    users = User.objects.all().values('id', 'name', 'email').order_by('id')
    return JsonResponse({"users": list(users)})


@csrf_exempt
def set_responsible(request):
    """
        Método para alterar o responsável da requisição de arte.
    :param request:
    :return Json com status da requsição:
    """
    if request.method == 'POST':
        art_request_id = request.POST.get('art_request_id')
        responsible_id = request.POST.get('responsible_id')
        if art_request_id and responsible_id:
            responsible = User.objects.get(id=responsible_id)
            if responsible:
                ArtRequestEvent.insert_art_event(
                    art_request_id=art_request_id,
                    event='ChangeResponsible',
                    value=responsible.get_short_name(),
                    user=request.user
                )
                ArtRequest.objects.filter(id=art_request_id).update(responsible=responsible.id)
                messages.add_message(request, messages.SUCCESS, 'New responsible assigned to request')
                return JsonResponse({'status': 'success'})


@csrf_exempt
def insert_message(request):
    """
        Método para inserir um comentário na requisição de arte.
    :param request:
    :return Json com status da requsição:
    """

    if request.method == 'POST':
        art_request_id = request.POST.get('art_request_id')
        message = request.POST.get('message')
        if art_request_id and message:
            ArtRequestEvent.insert_art_event(
                art_request_id=art_request_id,
                event='InsertComment',
                value=message,
                user=request.user
            )
            messages.add_message(request, messages.SUCCESS, 'New comment entered')
            return JsonResponse({'status': 'success'})


@csrf_exempt
def change_status(request):
    """
        Método para alterar o status da requisição
    :param request:
    :return:
    """
    if request.method == 'POST':
        art_request_id = request.POST.get('art_request_id')
        status = request.POST.get('status')
        if art_request_id and status:
            status_id = [item for item in STATUS_CHOICES if item[1] == status][0][0]
            ArtRequestEvent.insert_art_event(
                art_request_id=art_request_id,
                event='ChangeStatus',
                value=status_id,
                user=request.user
            )
            ArtRequest.objects.filter(id=art_request_id).update(status=status_id)
            if status == 'Completed':
                ArtRequestEvent.insert_art_event(
                    art_request_id=art_request_id,
                    event='ChangeProgress',
                    value=100,
                    user=request.user
                )
            messages.add_message(request, messages.SUCCESS, 'Status successfully changed')
            return JsonResponse({'status': 'success'})
