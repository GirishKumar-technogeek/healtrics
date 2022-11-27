from django.urls import path
from . import views

urlpatterns = [
    path('add_profile/',views.add_profile,name='add_blood_bank_profile'),
    path('edit_profile/',views.edit_profile,name='edit_blood_bank_profile'),
    path('view_profile/',views.view_profile,name='view_blood_bank_profile'),
    path('organize_camp/',views.organize_camp,name='organize_camp'),
    path('see_camps_blood_banks/',views.see_blood_bank_camps,name='see_camps_blood_banks'),
    path('view_camp_enrollments/<camp_id>/',views.view_camp_enrollments,name='view_camp_enrollments'),
    path('accept_blood_donation_from_donor_for_camp/<enrollment_id>/',views.accept_blood_donation_from_donor_for_camp,name='accept_blood_donation_from_donor_for_camp'),
    path('my_inventory/',views.my_inventory,name='my_inventory'),
    path('update_inventory/',views.update_inventory,name='update_inventory'),
    path('view_blood_requests/',views.view_blood_requests,name='view_blood_requests_blood_banks'),
    path('accept_blood_request/<request_id>/',views.accept_blood_request,name='accept_blood_request_blood_bank'),
    path('get_bdb_data_blood_bank/<request_id>/<blood_bank_id>/',views.get_bdb_data_blood_bank,name='get_bdb_data_blood_bank'),
    path('my_notifications/',views.my_notifications,name='my_notifications_blood_banks')
]