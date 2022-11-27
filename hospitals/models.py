from django.db import models
import uuid
from accounts.models import User
from blood_banks.models import BloodBankProfile
from donors.models import DonorProfile

BLOOD_TYPES = [('A+','A+'),('A-','A-'),('B+','B+'),('B-','B-'),('O+','O+'),('O-','O-'),('AB+','AB+'),('AB-','AB-')]
BLOOD_DONATION_TYPE = [('Whole Blood','Whole Blood'),('Red Cells','Red Cells'),('Platelets','Platelets'),('Plasma','Plasma')]
REQUEST_STATUS = [('Requested','Requested'),('Accepted','Accepted'),('Donated','Donated')]

class HospitalProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    hospital_name = models.TextField()
    address = models.TextField()
    area = models.TextField(null=True)
    state = models.TextField()
    city = models.TextField()
    country = models.TextField()
    zipcode = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    contact_email_address = models.EmailField(max_length=500)
    contact_mobile_number = models.TextField()
    website_url = models.URLField(max_length=500)
    logo = models.ImageField(upload_to='images/')
    clinic_establishment_certificate = models.FileField(upload_to='certs/')
    companies_registration_act_certificate = models.FileField(upload_to='certs/')
    societies_registration_act_certificate = models.FileField(upload_to='certs/')
    bloodbank_operating_license_certificate = models.FileField(upload_to='certs/')
    certificate_of_accreditation = models.FileField(upload_to='certs/')
    is_hospital_verified = models.BooleanField(default=False)

class BloodRequest(models.Model):
    request_id = models.UUIDField(default=uuid.uuid4, editable=False)
    hospital_profile = models.ForeignKey(HospitalProfile,on_delete=models.SET_NULL,null=True)
    request_date_time = models.DateTimeField(auto_now_add=True)
    request_description = models.TextField()
    donation_type_needed = models.CharField(max_length=100,choices=BLOOD_DONATION_TYPE)
    blood_type_needed = models.CharField(max_length=100,choices=BLOOD_TYPES)
    quantity_needed = models.BigIntegerField(default=0)
    donation_uses = models.TextField()
    approx_time_for_donating = models.TextField()

class BloodRequestDonor(models.Model):
    blood_request = models.ForeignKey(BloodRequest,on_delete=models.SET_NULL,null=True)
    donor_profile = models.ForeignKey(DonorProfile,on_delete=models.SET_NULL,null=True)
    request_status = models.CharField(max_length=100,choices=REQUEST_STATUS,default="Requested")
    donor_accepted_date_time = models.DateTimeField(null=True)
    donation_date_time = models.DateTimeField(null=True)
    collected_quantity_in_cc = models.BigIntegerField(null=True)
    transaction_id = models.TextField(null=True)

class BloodRequestBloodBank(models.Model):
    blood_request = models.ForeignKey(BloodRequest,on_delete=models.SET_NULL,null=True)
    blood_bank_profile = models.ForeignKey(BloodBankProfile,on_delete=models.SET_NULL,null=True)
    request_status = models.CharField(max_length=100,choices=REQUEST_STATUS,default="Requested")
    blood_bank_accepted_date_time = models.DateTimeField(null=True)
    donation_date_time = models.DateTimeField(null=True)
    collected_quantity_in_cc = models.BigIntegerField(null=True)
    transaction_id = models.TextField(null=True)