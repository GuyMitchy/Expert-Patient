from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from datetime import date
from .models import Medication
from .forms import MedicationForm

class MedicationListView(LoginRequiredMixin, ListView):
    model = Medication
    template_name = 'medications/list.html'
    context_object_name = 'medications'
    
    def get_queryset(self):
        return Medication.objects.filter(user=self.request.user)

class MedicationCreateView(LoginRequiredMixin, CreateView):
    model = Medication
    form_class = MedicationForm  # Use our custom form instead of fields
    template_name = 'medications/add.html'
    success_url = reverse_lazy('medications:list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = date.today()
        return context
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
