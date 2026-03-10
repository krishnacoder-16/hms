from django.db import models
from accounts.models import User
from doctors.models import Availability

class Booking(models.Model):
    STATUS_CHOICES = (
        ('BOOKED', 'Booked'),
        ('CANCELLED', 'Cancelled'),
    )
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_bookings')
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_bookings')
    availability_slot = models.ForeignKey(Availability, on_delete=models.CASCADE, related_name='bookings')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='BOOKED')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking for {self.patient.first_name} with Dr. {self.doctor.first_name} on {self.availability_slot.date}"
