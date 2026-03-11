from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.forms import SignupForm, LoginForm
from accounts.models import User
from hms_project.utils import send_email_notification

def signup_view(request):
    if request.user.is_authenticated:
        return redirect("accounts_home")

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_email_notification({
                "type": "SIGNUP_WELCOME",
                "email": user.email,
                "name": f"{user.first_name} {user.last_name}".strip() or "User"
            })
            messages.success(request, "Account created successfully. Please log in.")
            return redirect("login")
    else:
        form = SignupForm()
    
    return render(request, "signup.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        if request.user.role == User.Role.DOCTOR:
            return redirect("doctor_dashboard")
        elif request.user.role == User.Role.PATIENT:
            return redirect("patient_dashboard")
        else:
            # Fallback for superusers/receptionists
            return redirect("admin:index")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                if user.role == User.Role.DOCTOR:
                    return redirect("doctor_dashboard")
                elif user.role == User.Role.PATIENT:
                    return redirect("patient_dashboard")
                else:
                    return redirect("admin:index")
            else:
                messages.error(request, "Invalid email or password.")
    else:
        form = LoginForm()
        
    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("login")


@login_required
def doctor_dashboard(request):
    if request.user.role != User.Role.DOCTOR:
        messages.error(request, "You do not have permission to access the Doctor Dashboard.")
        return redirect("login")
    return render(request, "doctor_dashboard.html")


@login_required
def patient_dashboard(request):
    if request.user.role != User.Role.PATIENT:
        messages.error(request, "You do not have permission to access the Patient Dashboard.")
        return redirect("login")
    return render(request, "patient_dashboard.html")
