from django.urls import path
from . import views

urlpatterns = [
    path('add-slot/', views.add_availability, name='add_availability'),
    path('my-slots/', views.doctor_slots, name='doctor_slots'),
    path('delete-slot/<int:id>/', views.delete_slot, name='delete_slot'),
]
