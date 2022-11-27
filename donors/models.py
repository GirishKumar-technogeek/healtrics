from django.db import models
from accounts.models import User

BLOOD_TYPES = [('A+','A+'),('A-','A-'),('B+','B+'),('B-','B-'),('O+','O+'),('O-','O-'),('AB+','AB+'),('AB-','AB-')]
BLOOD_DONATION_TYPE = [('Whole Blood','Whole Blood'),('Red Cells','Red Cells'),('Platelets','Platelets'),('Plasma','Plasma')]

class DonorProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    full_name = models.TextField()
    gender = models.TextField()
    dob = models.DateField()
    blood_group = models.CharField(max_length=100,choices=BLOOD_TYPES)
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
    profile_pic = models.ImageField(upload_to='images/')
    first_donation_date = models.DateField(null=True)
    last_donation_date = models.DateField(null=True)
    number_of_donations = models.IntegerField(default=0)
    blood_donated_in_cc = models.IntegerField(default=0)
    last_donation_type = models.CharField(max_length=100,choices=BLOOD_DONATION_TYPE,null=True)    