from django.urls import path
from . import views

urlpatterns = [
    path('verify_hospitals/',views.verify_hospitals,name='verify_hospitals'),
    path('verify_blood_banks/',views.verify_blood_banks,name='verify_blood_banks'),
    path('verify_hospital/<hospital_id>/',views.verify_hospital,name='verify_hospital'),
    path('verify_blood_bank/<blood_bank_id>/',views.verify_blood_bank,name='verify_blood_bank')
]