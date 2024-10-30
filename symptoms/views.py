from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from datetime import date
from .models import Symptom

class SymptomListView(LoginRequiredMixin, ListView):
    model = Symptom
    template_name = 'symptoms/list.html'
    context_object_name = 'symptoms'
    
    def get_queryset(self):
        return Symptom.objects.filter(user=self.request.user)

class SymptomCreateView(LoginRequiredMixin, CreateView):
    model = Symptom
    template_name = 'symptoms/add.html'
    fields = ['date', 'type', 'severity', 'description']
    success_url = reverse_lazy('symptoms:list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = date.today()
        return context
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
