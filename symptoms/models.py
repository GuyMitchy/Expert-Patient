from django.db import models
from django.conf import settings

class Symptom(models.Model):
    SEVERITY_CHOICES = [(i, str(i)) for i in range(1, 11)]
    
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, 
                              on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    severity = models.IntegerField(choices=SEVERITY_CHOICES)
    description = models.TextField()
    location = models.CharField(max_length=100)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.patient.username} - {self.date.date()}" 