from django.db import models
from django.conf import settings

class Medication(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    common_dosages = models.JSONField(default=list)
    side_effects = models.TextField(blank=True)
    interactions = models.TextField(blank=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

class PatientMedication(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, 
                              on_delete=models.CASCADE)
    medication = models.ForeignKey(Medication, on_delete=models.PROTECT)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.patient.username} - {self.medication.name}"

class MedicationLog(models.Model):
    EFFECTIVENESS_CHOICES = [(i, str(i)) for i in range(1, 6)]
    
    patient_medication = models.ForeignKey(PatientMedication, 
                                         on_delete=models.CASCADE)
    taken_at = models.DateTimeField()
    taken_dosage = models.CharField(max_length=100)
    symptoms_at_time = models.TextField(blank=True)
    effectiveness_rating = models.IntegerField(
        choices=EFFECTIVENESS_CHOICES,
        null=True,
        blank=True
    )
    side_effects_noted = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-taken_at']
    
    def __str__(self):
        return f"{self.patient_medication} - {self.taken_at}" 