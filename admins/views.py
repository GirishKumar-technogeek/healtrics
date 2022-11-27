from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required,user_passes_test
from accounts.views import check_admins
from hospitals.models import HospitalProfile
from blood_banks.models import BloodBankProfile

@login_required
@user_passes_test(test_func=check_admins,login_url='/accounts/admins_login')
def verify_hospitals(request):
    hospitals = HospitalProfile.objects.filter().all()
    return render(request,'admins/verify_hospitals.html',{'hospitals':hospitals})

@login_required
@user_passes_test(test_func=check_admins,login_url='/accounts/admins_login')
def verify_hospital(request,hospital_id):
    hospital = HospitalProfile.objects.filter(user__user_id=hospital_id).first()
    hospital.is_hospital_verified = True
    hospital.save()
    return redirect('verify_hospitals')

@login_required
@user_passes_test(test_func=check_admins,login_url='/accounts/admins_login')
def verify_blood_banks(request):
    blood_banks = BloodBankProfile.objects.filter().all()
    return render(request,'admins/verify_blood_banks.html',{'blood_banks':blood_banks})

@login_required
@user_passes_test(test_func=check_admins,login_url='/accounts/admins_login')
def verify_blood_bank(request,blood_bank_id):
    blood_bank = BloodBankProfile.objects.filter(user__user_id=blood_bank_id).first()
    blood_bank.is_blood_bank_verified = True
    blood_bank.save()
    return redirect('verify_blood_banks')