from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required,user_passes_test
from accounts.views import check_hospitals,get_coordinates, getApproxTimeForDonating, getDonationUses,isSuitableDonorByType, sendMail, sendSMS, writeBDB
from django.conf import settings
from django.db.models.functions import Radians, Power, Sin, Cos, ATan2, Sqrt, Radians
from django.db.models import F
import datetime,requests,numpy as np
from .models import HospitalProfile,BloodRequest,BloodRequestDonor,BloodRequestBloodBank
from accounts.models import Notification
from blood_banks.models import BloodBankInventory, BloodBankProfile
from donors.models import DonorProfile

@login_required
@user_passes_test(test_func=check_hospitals,login_url='/accounts/hospitals_login')
def add_profile(request):
    if request.method == 'POST':
        hospital_name=request.POST['hospital_name']
        address=request.POST['address']
        area=request.POST['area']
        state=request.POST['state']
        city=request.POST['city']
        country=request.POST['country']
        zipcode=request.POST['zipcode']
        coords = get_coordinates(address, area , city, state, country)
        if coords is None:
            return render(request,'hospitals/add_profile.html')
        latitude=coords[0]
        longitude=coords[1]
        contact_email_address=request.POST['contact_email_address']
        contact_mobile_number=request.POST['contact_mobile_number']
        website_url=request.POST['website_url']
        hospital = HospitalProfile(user=request.user,hospital_name=hospital_name,address=address,area=area,city=city,state=state,country=country,zipcode=zipcode,latitude=latitude,longitude=longitude,contact_email_address=contact_email_address,contact_mobile_number=contact_mobile_number,website_url=website_url,logo=request.FILES['logo'],clinic_establishment_certificate=request.FILES['clinic_establishment_certificate'],companies_registration_act_certificate=request.FILES['companies_registration_act_certificate'],societies_registration_act_certificate=request.FILES['societies_registration_act_certificate'],bloodbank_operating_license_certificate=request.FILES['bloodbank_operating_license_certificate'],certificate_of_accreditation=request.FILES['certificate_of_accreditation'])
        hospital.save()
        return redirect('view_hospital_profile')
    else:
        return render(request,'hospitals/add_profile.html')

@login_required
@user_passes_test(test_func=check_hospitals,login_url='/accounts/hospitals_login')
def edit_profile(request):
    if request.method == 'POST':
        hospital=HospitalProfile.objects.filter(user=request.user).first()
        hospital.hospital_name=request.POST['hospital_name']
        hospital.address=request.POST['address']
        hospital.area=request.POST['area']
        hospital.state=request.POST['state']
        hospital.city=request.POST['city']
        hospital.country=request.POST['country']
        hospital.zipcode=request.POST['zipcode']
        coords = get_coordinates(request.POST['address'], request.POST['area'] ,request.POST['city'], request.POST['state'], request.POST['country'])
        hospital.latitude=coords[0]
        hospital.longitude=coords[1]
        hospital.contact_email_address=request.POST['contact_email_address']
        hospital.contact_mobile_number=request.POST['contact_mobile_number']
        hospital.website_url=request.POST['website_url']
        hospital.save()
        return redirect('view_hospital_profile')
    else:
        hospital=HospitalProfile.objects.filter(user=request.user).first()
        return render(request,'hospitals/edit_profile.html',{'hospital':hospital})

@login_required
@user_passes_test(test_func=check_hospitals,login_url='/accounts/hospitals_login')
def view_profile(request):
    hospital=HospitalProfile.objects.filter(user=request.user).first()
    return render(request,'hospitals/view_profile.html',{'hospital':hospital})

@login_required
@user_passes_test(test_func=check_hospitals,login_url='/accounts/hospitals_login')
def request_for_blood(request):
    if request.method == 'POST':
        hospital_profile = HospitalProfile.objects.filter(user=request.user).first()
        request_description = request.POST['request_description']
        donation_type_needed = request.POST['donation_type_needed']
        blood_type_needed = request.POST['blood_type_needed']
        quantity_needed = int(request.POST['quantity_needed'])
        donation_uses = getDonationUses(donation_type_needed)
        approx_time_for_donating = getApproxTimeForDonating(donation_type_needed)
        blood_request = BloodRequest(hospital_profile=hospital_profile,request_description=request_description,donation_type_needed=donation_type_needed,blood_type_needed=blood_type_needed,quantity_needed=quantity_needed,donation_uses=donation_uses,approx_time_for_donating=approx_time_for_donating)
        blood_request.save()
        dlat = Radians(F('latitude') - hospital_profile.latitude)
        dlong = Radians(F('longitude') - hospital_profile.longitude)
        a = (Power(Sin(dlat/2), 2) + Cos(Radians(hospital_profile.latitude)) * Cos(Radians(F('latitude'))) * Power(Sin(dlong/2), 2))
        c = 2 * ATan2(Sqrt(a), Sqrt(1-a))
        d = 6371 * c
        blood_banks = BloodBankProfile.objects.annotate(distance=d).order_by('distance').filter(distance__lt=10)
        for blood_bank in blood_banks:
            BloodRequestBloodBank(blood_request=blood_request,blood_bank_profile=blood_bank).save()
            Notification(user=blood_bank.user,message="Healtrics Blood Request!!!You got a blood request!!! Please visit your profile!!!").save()
        donors = DonorProfile.objects.annotate(distance=d).order_by('distance').filter(distance__lt=10,blood_group__in=isSuitableDonorByType(donation_type_needed,blood_type_needed))
        for donor in donors:
            #if (datetime.date.today() - donor.last_donation_date).days > (donor.last_donation_date - donor.first_donation_date).days / donor.number_of_donations
            #if donor.last_donation_date is None or (datetime.date.today() - donor.last_donation_date).days > 56 :
            BloodRequestDonor(blood_request=blood_request,donor_profile=donor).save()
            Notification(user=donor.user,message="Healtrics Blood Request!!!You got a blood request!!! Please visit your profile!!!").save()
        return redirect('view_hospital_blood_requests')
    else:
        return render(request,'hospitals/request_for_blood.html')

@login_required
@user_passes_test(test_func=check_hospitals,login_url='/accounts/hospitals_login')
def view_blood_requests(request):
    hospital_profile = HospitalProfile.objects.filter(user=request.user).first()
    blood_requests = BloodRequest.objects.filter(hospital_profile=hospital_profile).order_by('-request_date_time').all()
    return render(request,'hospitals/view_blood_requests.html',{'blood_requests':blood_requests})

@login_required
@user_passes_test(test_func=check_hospitals,login_url='/accounts/hospitals_login')
def view_requested_donors(request,request_id):
    hospital_profile = HospitalProfile.objects.filter(user=request.user).first()
    dlat = Radians(F('donor_profile__latitude') - hospital_profile.latitude)
    dlong = Radians(F('donor_profile__longitude') - hospital_profile.longitude)
    a = (Power(Sin(dlat/2), 2) + Cos(Radians(hospital_profile.latitude)) * Cos(Radians(F('donor_profile__latitude'))) * Power(Sin(dlong/2), 2))
    c = 2 * ATan2(Sqrt(a), Sqrt(1-a))
    d = 6371 * c
    blood_request_donors = BloodRequestDonor.objects.filter(blood_request__request_id=request_id,request_status='Requested').annotate(distance=d).all()
    return render(request,'hospitals/view_requested_donors.html',{'blood_request_donors':blood_request_donors})

@login_required
@user_passes_test(test_func=check_hospitals,login_url='/accounts/hospitals_login')
def view_requested_blood_banks(request,request_id):
    hospital_profile = HospitalProfile.objects.filter(user=request.user).first()
    dlat = Radians(F('blood_bank_profile__latitude') - hospital_profile.latitude)
    dlong = Radians(F('blood_bank_profile__longitude') - hospital_profile.longitude)
    a = (Power(Sin(dlat/2), 2) + Cos(Radians(hospital_profile.latitude)) * Cos(Radians(F('blood_bank_profile__latitude'))) * Power(Sin(dlong/2), 2))
    c = 2 * ATan2(Sqrt(a), Sqrt(1-a))
    d = 6371 * c
    blood_request_blood_banks = BloodRequestBloodBank.objects.filter(blood_request__request_id=request_id,request_status='Requested').annotate(distance=d).all()
    return render(request,'hospitals/view_requested_blood_banks.html',{'blood_request_blood_banks':blood_request_blood_banks})

@login_required
@user_passes_test(test_func=check_hospitals,login_url='/accounts/hospitals_login')
def is_suitable_donor(request,donor_id):
    donor_profile = DonorProfile.objects.filter(user__user_id=donor_id).first()
    # recency = (datetime.date.today() - donor_profile.last_donation_date).days
    # frequency = donor_profile.number_of_donations
    # monetary = np.log(donor_profile.blood_donated_in_cc)
    # time = (datetime.date.today() - donor_profile.first_donation_date).days
    recency = 2
    frequency = 60
    monetary = 10000
    time = 80
    data = {
        "recency" : str(recency),
        "frequency" : str(frequency),
        "monetary" : str(monetary),
        "time" : str(time),
    }
    response = requests.get("http://localhost:5000/prediction",data)
    return render(request,'hospitals/is_suitable_donor.html',{'response':response.json().get('Prediction')})

@login_required
@user_passes_test(test_func=check_hospitals,login_url='/accounts/hospitals_login')
def sendEmailAlert(request,donor_id):
    donor = DonorProfile.objects.filter(user__user_id=donor_id).first()
    sendMail("Healtrics Blood Request!!!","You got a blood request!!! Please visit your profile!!!",settings.EMAIL_HOST_USER,[donor.user.email_address])
    return redirect('view_hospital_blood_requests')

@login_required
@user_passes_test(test_func=check_hospitals,login_url='/accounts/hospitals_login')
def sendSMSAlert(request,donor_id):
    donor = DonorProfile.objects.filter(user__user_id=donor_id).first()
    sendSMS("Healtrics !!!You got a blood request!!! Please visit your profile!!!",donor.user.mobile_number)
    return redirect('view_hospital_blood_requests')

@login_required
@user_passes_test(test_func=check_hospitals,login_url='/accounts/hospitals_login')
def view_requested_blood_bank_inventory(request,blood_bank_id):
    blood_bank = BloodBankProfile.objects.filter(user__user_id=blood_bank_id).first()
    blood_bank_inventory = BloodBankInventory.objects.filter(blood_bank=blood_bank).first()
    return render(request,'hospitals/view_requested_blood_bank_inventory.html',{'blood_bank_inventory':blood_bank_inventory})

@login_required
@user_passes_test(test_func=check_hospitals,login_url='/accounts/hospitals_login')
def view_accepted_donors(request,request_id):
    blood_request_donors = BloodRequestDonor.objects.filter(blood_request__request_id=request_id,request_status='Accepted').all()
    return render(request,'hospitals/view_accepted_donors.html',{'blood_request_donors':blood_request_donors})

@login_required
@user_passes_test(test_func=check_hospitals,login_url='/accounts/hospitals_login')
def view_accepted_blood_banks(request,request_id):
    blood_request_blood_banks = BloodRequestBloodBank.objects.filter(blood_request__request_id=request_id,request_status='Accepted').all()
    return render(request,'hospitals/view_accepted_blood_banks.html',{'blood_request_blood_banks':blood_request_blood_banks})

@login_required
@user_passes_test(test_func=check_hospitals,login_url='/accounts/hospitals_login')
def accept_blood_donation_from_donor(request,request_id,donor_id):
    blood_request = BloodRequest.objects.filter(request_id=request_id).first()
    donor_profile = DonorProfile.objects.filter(user__user_id=donor_id).first()
    blood_request_donor = BloodRequestDonor.objects.filter(blood_request=blood_request,donor_profile=donor_profile).first()
    blood_request_donor.request_status = 'Donated'
    blood_request_donor.donation_date_time = datetime.datetime.now()
    blood_request_donor.collected_quantity_in_cc = int(request.GET['collected_quantity_in_cc'])
    data = {
        "request_id" : str(request_id),
        "donor_type" : 'Donor',
        "blood_bank_id" : 'null',
        "donor_id" : str(donor_id),
        "donation_date_time" : str(datetime.datetime.now()),
        "donation_type" : blood_request.donation_type_needed,
        "blood_type" : donor_profile.blood_group,
        "donated_quantity" : str(request.GET['collected_quantity_in_cc'])
    }
    transaction_id = writeBDB(data)
    blood_request_donor.transaction_id = transaction_id
    blood_request_donor.save()
    donor_profile = blood_request_donor.donor_profile
    if donor_profile.first_donation_date is None:
        donor_profile.first_donation_date = datetime.date.today()
    donor_profile.last_donation_date = datetime.date.today()
    donor_profile.number_of_donations += 1
    donor_profile.blood_donated_in_cc += int(request.GET['collected_quantity_in_cc'])
    donor_profile.last_donation_type = blood_request.donation_type_needed
    donor_profile.save()
    return redirect('view_hospital_blood_requests')

@login_required
@user_passes_test(test_func=check_hospitals,login_url='/accounts/hospitals_login')
def accept_blood_donation_from_blood_bank(request,request_id,blood_bank_id):
    blood_request = BloodRequest.objects.filter(request_id=request_id).first()
    blood_bank_profile = BloodBankProfile.objects.filter(user__user_id=blood_bank_id).first()
    blood_request_blood_bank = BloodRequestBloodBank.objects.filter(blood_request=blood_request,blood_bank_profile=blood_bank_profile).first()
    blood_request_blood_bank.request_status = 'Donated'
    blood_request_blood_bank.donation_date_time = datetime.datetime.now()
    blood_request_blood_bank.collected_quantity_in_cc = int(request.GET['collected_quantity_in_cc'])
    data = {
        "request_id" : str(request_id),
        "donor_type" : 'Blood Bank',
        "blood_bank_id" : str(blood_bank_id),
        "donor_id" : 'null',
        "donation_date_time" : str(datetime.datetime.now()),
        "donation_type" : blood_request.donation_type_needed,
        "blood_type" : blood_request.blood_type_needed,
        "donated_quantity" : str(request.GET['collected_quantity_in_cc'])
    }
    transaction_id = writeBDB(data)
    blood_request_blood_bank.transaction_id = transaction_id
    blood_request_blood_bank.save()
    return redirect('view_hospital_blood_requests')

@login_required
@user_passes_test(test_func=check_hospitals,login_url='/accounts/hospitals_login')
def view_blood_donations_from_donors(request):
    hospital_profile = HospitalProfile.objects.filter(user=request.user).first()
    blood_request_donors = BloodRequestDonor.objects.filter(blood_request__hospital_profile=hospital_profile,request_status='Donated').all()
    return render(request,'hospitals/view_blood_donations_from_donors.html',{'blood_request_donors':blood_request_donors})

@login_required
@user_passes_test(test_func=check_hospitals,login_url='/accounts/hospitals_login')
def view_blood_donations_from_blood_banks(request):
    hospital_profile = HospitalProfile.objects.filter(user=request.user).first()
    blood_request_blood_banks = BloodRequestBloodBank.objects.filter(blood_request__hospital_profile=hospital_profile,request_status='Donated').all()
    return render(request,'hospitals/view_blood_donations_from_blood_banks.html',{'blood_request_blood_banks':blood_request_blood_banks})