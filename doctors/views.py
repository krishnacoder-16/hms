from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import User
from doctors.models import Availability
from doctors.forms import AvailabilityForm

def is_doctor(user):
    return user.is_authenticated and user.role == User.Role.DOCTOR

@login_required
def add_availability(request):
    if not is_doctor(request.user):
        messages.error(request, "Only doctors can access this page.")
        return redirect("login")

    if request.method == "POST":
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            availability = form.save(commit=False)
            availability.doctor = request.user
            
            # Check for duplicate
            if Availability.objects.filter(
                doctor=request.user, 
                date=availability.date, 
                start_time=availability.start_time, 
                end_time=availability.end_time
            ).exists():
                messages.error(request, "This time slot already exists.")
            else:
                availability.save()
                messages.success(request, "Availability slot added successfully!")
                return redirect("doctor_slots")
    else:
        form = AvailabilityForm()

    return render(request, "add_slot.html", {"form": form})


@login_required
def doctor_slots(request):
    if not is_doctor(request.user):
        messages.error(request, "Only doctors can access this page.")
        return redirect("login")

    slots = Availability.objects.filter(doctor=request.user).order_by('date', 'start_time')
    return render(request, "my_slots.html", {"slots": slots})


@login_required
def delete_slot(request, id):
    if not is_doctor(request.user):
        messages.error(request, "Only doctors can access this page.")
        return redirect("login")

    slot = get_object_or_404(Availability, id=id, doctor=request.user)
    
    if request.method == "POST":
        slot.delete()
        messages.success(request, "Slot deleted successfully.")
        return redirect("doctor_slots")
    
    # Alternatively we can also just delete and redirect on GET if simple enough
    # but POST is safer. Let's redirect if visited via GET
    return redirect("doctor_slots")
