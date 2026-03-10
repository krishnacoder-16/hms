from django.db import models
from accounts.models import User
from doctors.models import Availability

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
        ('COMPLETED', 'Completed'),
    )
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    availability_slot = models.OneToOneField(Availability, on_delete=models.SET_NULL, null=True)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appointment: {self.patient.email} at {self.availability_slot}"
