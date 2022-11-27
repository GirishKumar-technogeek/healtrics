from django.urls import path
from . import views

urlpatterns = [
    path('add_profile/',views.add_profile,name='add_donor_profile'),
    path('edit_profile/',views.edit_profile,name='edit_donor_profile'),
    path('view_profile/',views.view_profile,name='view_donor_profile'),
    path('see_camps_donors/',views.see_camps_donors,name='see_camps_donors'),
    path('enroll_in_camp/<camp_id>/',views.enroll_in_camp,name='enroll_in_camp'),
    path('enrolled_camps/',views.enrolled_camps,name='enrolled_camps'),
    path('view_blood_requests/',views.view_blood_requests,name='view_blood_requests_donors'),
    path('accept_blood_request/<request_id>/',views.accept_blood_request,name='accept_blood_request_donor'),
    path('get_bdb_data_donor/<request_id>/',views.get_bdb_data_donors,name='get_bdb_data_donor'),
    path('my_notifications/',views.my_notifications,name='my_notifications_donors'),
]