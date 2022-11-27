from django.db import models
import uuid
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class MyUserManager(BaseUserManager):
    def create_user(self, email_address, mobile_number, password=None):
        if not email_address:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have a password')
        if not mobile_number:
            raise ValueError('Users must have a mobile number')
        user = self.model(
            email_address=self.normalize_email(email_address),
            mobile_number=mobile_number
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email_address,mobile_number,password=None):
        user = self.create_user(
            email_address,
            mobile_number,
            password=password,
        )
        user.is_admin = True
        user.is_email_verified = True
        user.is_mobile_verified = True
        user.save(using=self._db)
        return user

USER_TYPES = [('Admin','Admin'),('Hospital','Hospital'),('Blood Bank','Blood Bank'),('Donor','Donor')]

class User(AbstractBaseUser):
    email_address = models.EmailField(max_length=500,unique=True)
    mobile_number = models.TextField()
    user_type = models.CharField(max_length=500, choices = USER_TYPES,default="Admin")
    user_id = models.UUIDField(default=uuid.uuid4, editable=False)
    email_code = models.CharField(max_length=10, null=True)
    mobile_code = models.CharField(max_length=10, null=True)
    is_email_verified = models.BooleanField(default=False)
    is_mobile_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_date_time = models.DateTimeField(auto_now_add=True)
    objects = MyUserManager()
    USERNAME_FIELD = 'email_address'
    REQUIRED_FIELDS = ['mobile_number']

    def __str__(self):
        return self.email_address

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

class Notification(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    message = models.TextField()
    added_date_time = models.DateTimeField(auto_now_add=True)