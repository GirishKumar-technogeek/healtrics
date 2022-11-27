from django.db import models
import uuid
from accounts.models import User
from donors.models import DonorProfile

CAMP_STATUS = [('Enrolled','Enrolled'),('Donated','Donated')]
BLOOD_TYPES = [('A+','A+'),('A-','A-'),('B+','B+'),('B-','B-'),('O+','O+'),('O-','O-'),('AB+','AB+'),('AB-','AB-')]

class BloodBankProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    blood_bank_name = models.TextField()
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
    bloodbank_operating_license_certificate = models.FileField(upload_to='certs/')
    certificate_of_accreditation = models.FileField(upload_to='certs/')
    is_blood_bank_verified = models.BooleanField(default=False)

class BloodCamp(models.Model):
    blood_bank = models.ForeignKey(BloodBankProfile,on_delete=models.CASCADE)
    camp_id = models.UUIDField(default=uuid.uuid4, editable=False)
    camp_description = models.TextField()
    camp_date = models.DateField()
    camp_time = models.TimeField()
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
    team_size = models.IntegerField()
    camp_brochure = models.FileField(upload_to='camps/')

class BloodBankInventory(models.Model):
    blood_bank = models.OneToOneField(BloodBankProfile,on_delete=models.CASCADE)
    a_plus_in_cc = models.BigIntegerField()
    a_minus_in_cc = models.BigIntegerField()
    b_plus_in_cc = models.BigIntegerField()
    b_minus_in_cc = models.BigIntegerField()
    o_plus_in_cc = models.BigIntegerField()
    o_minus_in_cc = models.BigIntegerField()
    ab_plus_in_cc = models.BigIntegerField()
    ab_minus_in_cc = models.BigIntegerField()
    updated_date_time = models.DateTimeField(auto_now=True)

class BloodCampEnrollment(models.Model):
    blood_camp = models.ForeignKey(BloodCamp,on_delete=models.CASCADE)
    donor_profile = models.ForeignKey(DonorProfile,on_delete=models.CASCADE)
    enrollment_id = models.UUIDField(default=uuid.uuid4, editable=False)
    camp_enrollment_status = models.CharField(max_length=100,choices=CAMP_STATUS,default='Enrolled')
    enrolled_date_time = models.DateTimeField(auto_now_add=True)
    donation_date_time = models.DateTimeField(null=True)
    blood_group_collected = models.CharField(max_length=100,choices=BLOOD_TYPES,null=True)
    collected_quantity_in_cc = models.BigIntegerField(null=True)
    transaction_id = models.TextField(null=True)