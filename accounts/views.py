from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required


def signup_view(request):
    return render(request, "signup.html")


def login_view(request):
    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def doctor_dashboard(request):
    return render(request, "doctor_dashboard.html")


@login_required
def patient_dashboard(request):
    return render(request, "patient_dashboard.html")