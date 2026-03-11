from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db import transaction
from accounts.models import User
from doctors.models import Availability
from bookings.models import Booking
from hms_project.utils import send_email_notification

def is_patient(user):
    return user.is_authenticated and user.role == User.Role.PATIENT

@login_required
def doctor_list(request):
    if not is_patient(request.user):
        messages.error(request, "Only patients can access this page.")
        return redirect("login")

    # Get all users with the role of DOCTOR
    doctors = User.objects.filter(role=User.Role.DOCTOR).order_by('first_name', 'last_name')
    return render(request, "doctor_list.html", {"doctors": doctors})

@login_required
def doctor_slots(request, doctor_id):
    if not is_patient(request.user):
        messages.error(request, "Only patients can access this page.")
        return redirect("login")

    doctor = get_object_or_404(User, id=doctor_id, role=User.Role.DOCTOR)
    
    # Get future available slots for this doctor
    slots = Availability.objects.filter(
        doctor=doctor, 
        is_booked=False,
        date__gte=timezone.now().date()
    ).order_by('date', 'start_time')
    
    return render(request, "doctor_slots.html", {"doctor": doctor, "slots": slots})

@login_required
def book_slot(request, slot_id):
    if not is_patient(request.user):
        messages.error(request, "Only patients can book appointments.")
        return redirect("login")

    if request.method == "POST":
        
        # Use database transaction to avoid race conditions
        with transaction.atomic():
            slot = get_object_or_404(Availability, id=slot_id)
            
            # Additional check to ensure it's not in the past
            if slot.date < timezone.now().date():
                 messages.error(request, "This slot is in the past and cannot be booked.")
                 return redirect("doctor_slots", doctor_id=slot.doctor.id)

            if slot.is_booked:
                messages.error(request, "Sorry, this slot is already booked.")
            else:
                # Mark as booked
                slot.is_booked = True
                slot.save()
                
                # Create booking
                Booking.objects.create(
                    doctor=slot.doctor,
                    patient=request.user,
                    availability_slot=slot,
                    status='BOOKED'
                )
                
                send_email_notification({
                    "type": "BOOKING_CONFIRMATION",
                    "email": request.user.email,
                    "name": f"{request.user.first_name} {request.user.last_name}".strip() or "Patient",
                    "doctor": f"{slot.doctor.first_name} {slot.doctor.last_name}".strip(),
                    "date": slot.date.strftime("%Y-%m-%d"),
                    "time": f"{slot.start_time.strftime('%I:%M %p')} - {slot.end_time.strftime('%I:%M %p')}"
                })
                
                messages.success(request, f"Successfully booked appointment with Dr. {slot.doctor.last_name} on {slot.date} at {slot.start_time}.")
                return redirect("my_appointments")
                
    # If accessed via GET, redirect back to doctor list or dashboard
    return redirect("doctor_list")

@login_required
def my_appointments(request):
    if not is_patient(request.user):
        messages.error(request, "Only patients can access this page.")
        return redirect("login")

    appointments = Booking.objects.filter(patient=request.user).order_by('-created_at')
    return render(request, "my_appointments.html", {"appointments": appointments})
