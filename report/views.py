# Create your views here.
from django.views.generic import TemplateView

from report.models import AverageWorkTime


class AverageWorkTimeView(TemplateView):
    template_name = 'report/average_worktime.html'

    def get_context_data(self, **kwargs):
        context = super(AverageWorkTimeView, self).get_context_data(**kwargs)
        context['page_title'] = 'DafitiArt | Average Work Time Report'
        context['objects'] = AverageWorkTime.objects.all().order_by('work_average')
        return context
