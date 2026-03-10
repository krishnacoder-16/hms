from django.db import models
from accounts.models import User

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    specialty = models.CharField(max_length=100)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name} - {self.specialty}"

class Availability(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='availabilities')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date', 'start_time']
        unique_together = ('doctor', 'date', 'start_time', 'end_time')

    def __str__(self):
        return f"{self.doctor.first_name} {self.doctor.last_name} - {self.date} {self.start_time}-{self.end_time}"
