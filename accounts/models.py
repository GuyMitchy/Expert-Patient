from django.contrib.auth.models import AbstractUser
from django.db import models

class Patient(AbstractUser):
    date_of_diagnosis = models.DateField(null=True, blank=True)
    current_medications = models.TextField(blank=True)
    
    def __str__(self):
        return self.username 