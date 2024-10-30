from django.urls import path
from . import views

app_name = 'medications'

urlpatterns = [
    path('', views.MedicationListView.as_view(), name='list'),
    path('add/', views.MedicationCreateView.as_view(), name='add'),
] 