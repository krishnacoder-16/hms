from django.urls import path
from . import views

urlpatterns = [
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctor/<int:doctor_id>/slots/', views.doctor_slots, name='doctor_slots_list'),
    path('book/<int:slot_id>/', views.book_slot, name='book_slot'),
    path('my-appointments/', views.my_appointments, name='my_appointments'),
]
