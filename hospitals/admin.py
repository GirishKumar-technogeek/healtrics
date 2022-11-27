from django.contrib import admin
from .models import *

admin.site.register(HospitalProfile)
admin.site.register(BloodRequest)
admin.site.register(BloodRequestDonor)
admin.site.register(BloodRequestBloodBank)