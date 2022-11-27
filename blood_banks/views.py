import datetime,requests,json
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required,user_passes_test
from accounts.views import check_blood_banks,get_coordinates,writeBDB
from .models import BloodBankProfile,BloodCamp,BloodCampEnrollment,BloodBankInventory
from accounts.models import Notification
from hospitals.models import BloodRequest, BloodRequestBloodBank

@login_required
@user_passes_test(test_func=check_blood_banks,login_url='/accounts/blood_banks_login')
def add_profile(request):
    if request.method == 'POST':
        blood_bank_name=request.POST['blood_bank_name']
        address=request.POST['address']
        area=request.POST['area']
        state=request.POST['state']
        city=request.POST['city']
        country=request.POST['country']
        zipcode=request.POST['zipcode']
        coords = get_coordinates(address, area , city, state, country)
        if coords is None:
            return render(request,'blood_banks/add_profile.html')
        latitude=coords[0]
        longitude=coords[1]
        contact_email_address=request.POST['contact_email_address']
        contact_mobile_number=request.POST['contact_mobile_number']
        website_url=request.POST['website_url']
        blood_bank = BloodBankProfile(user=request.user,blood_bank_name=blood_bank_name,address=address,area=area,city=city,state=state,country=country,zipcode=zipcode,latitude=latitude,longitude=longitude,contact_email_address=contact_email_address,contact_mobile_number=contact_mobile_number,website_url=website_url,logo=request.FILES['logo'],bloodbank_operating_license_certificate=request.FILES['bloodbank_operating_license_certificate'],certificate_of_accreditation=request.FILES['certificate_of_accreditation'])
        blood_bank.save()
        return redirect('view_blood_bank_profile')
    else:
        return render(request,"blood_banks/add_profile.html")

@login_required
@user_passes_test(test_func=check_blood_banks,login_url='/accounts/blood_banks_login')
def edit_profile(request):
    if request.method == 'POST':
        blood_bank=BloodBankProfile.objects.filter(user=request.user).first()
        blood_bank.blood_bank_name=request.POST['blood_bank_name']
        blood_bank.address=request.POST['address']
        blood_bank.area=request.POST['area']
        blood_bank.state=request.POST['state']
        blood_bank.city=request.POST['city']
        blood_bank.country=request.POST['country']
        blood_bank.zipcode=request.POST['zipcode']
        coords = get_coordinates(request.POST['address'], request.POST['area'] ,request.POST['city'], request.POST['state'], request.POST['country'])
        blood_bank.latitude=coords[0]
        blood_bank.longitude=coords[1]
        blood_bank.contact_email_address=request.POST['contact_email_address']
        blood_bank.contact_mobile_number=request.POST['contact_mobile_number']
        blood_bank.website_url=request.POST['website_url']
        blood_bank.save()
        return redirect('view_blood_bank_profile')
    else:
        blood_bank=BloodBankProfile.objects.filter(user=request.user).first()
        return render(request,'blood_banks/edit_profile.html',{'blood_bank':blood_bank})

@login_required
@user_passes_test(test_func=check_blood_banks,login_url='/accounts/blood_banks_login')
def view_profile(request):
    blood_bank=BloodBankProfile.objects.filter(user=request.user).first()
    return render(request,'blood_banks/view_profile.html',{'blood_bank':blood_bank})

@login_required
@user_passes_test(test_func=check_blood_banks,login_url='/accounts/blood_banks_login')
def organize_camp(request):
    if request.method == 'POST':
        blood_bank=BloodBankProfile.objects.filter(user=request.user).first()
        camp_description=request.POST['camp_description']
        camp_date=request.POST['camp_date']
        camp_time=request.POST['camp_time']
        address=request.POST['address']
        area=request.POST['area']
        state=request.POST['state']
        city=request.POST['city']
        country=request.POST['country']
        zipcode=request.POST['zipcode']
        coords = get_coordinates(address , area , city ,  state ,  country)
        latitude=coords[0]
        longitude=coords[1]
        contact_email_address=request.POST['contact_email_address']
        contact_mobile_number=request.POST['contact_mobile_number']
        team_size=request.POST['team_size']
        blood_camp=BloodCamp(blood_bank=blood_bank,camp_description=camp_description,camp_date=camp_date,camp_time=camp_time,address=address,city=city,state=state,country=country,zipcode=zipcode,latitude=latitude,longitude=longitude,contact_email_address=contact_email_address,contact_mobile_number=contact_mobile_number,team_size=team_size,camp_brochure=request.FILES['camp_brochure'])
        blood_camp.save()
        return redirect('see_camps_blood_banks')
    else:
        return render(request,'blood_banks/organize_camp.html')

@login_required
@user_passes_test(test_func=check_blood_banks,login_url='/accounts/blood_banks_login')
def see_blood_bank_camps(request):
    blood_bank=BloodBankProfile.objects.filter(user=request.user).first()
    blood_camps = BloodCamp.objects.filter(blood_bank=blood_bank).all()
    return render(request,'blood_banks/see_blood_bank_camps.html',{'blood_camps':blood_camps})

@login_required
@user_passes_test(test_func=check_blood_banks,login_url='/accounts/blood_banks_login')
def view_camp_enrollments(request,camp_id):
    blood_camp_enrollments = BloodCampEnrollment.objects.filter(blood_camp__camp_id=camp_id).all()
    return render(request,'blood_banks/view_camp_enrollments.html',{'blood_camp_enrollments':blood_camp_enrollments})

@login_required
@user_passes_test(test_func=check_blood_banks,login_url='/accounts/blood_banks_login')
def accept_blood_donation_from_donor_for_camp(request,enrollment_id):
    blood_camp_enrollment = BloodCampEnrollment.objects.filter(enrollment_id=enrollment_id).first()
    blood_camp_enrollment.camp_enrollment_status = 'Donated'
    blood_camp_enrollment.donation_date_time = datetime.datetime.now()
    blood_camp_enrollment.blood_group_collected = blood_camp_enrollment.donor_profile.blood_group
    blood_camp_enrollment.collected_quantity_in_cc = request.GET['collected_quantity_in_cc']
    data = {
        "request_id" : str(enrollment_id),
        "donor_type" : 'Donor',
        "blood_bank_id" : str(blood_camp_enrollment.blood_camp.blood_bank.user.user_id),
        "donor_id" : str(blood_camp_enrollment.donor_profile.user.user_id),
        "donation_date_time" : str(datetime.datetime.now()),
        "donation_type" : 'Camp',
        "blood_type" : str(blood_camp_enrollment.donor_profile.blood_group),
        "donated_quantity" : str(request.GET['collected_quantity_in_cc'])
    }
    transaction_id = writeBDB(data)
    blood_camp_enrollment.transaction_id = transaction_id
    blood_camp_enrollment.save()
    donor_profile = blood_camp_enrollment.donor_profile
    if donor_profile.first_donation_date is None:
        donor_profile.first_donation_date = datetime.date.today()
    donor_profile.last_donation_date = datetime.date.today()
    donor_profile.number_of_donations += 1
    donor_profile.blood_donated_in_cc += int(request.GET['collected_quantity_in_cc'])
    donor_profile.last_donation_type = 'Whole Blood'
    donor_profile.save()
    return redirect('see_camps_blood_banks')

@login_required
@user_passes_test(test_func=check_blood_banks,login_url='/accounts/blood_banks_login')
def my_inventory(request):
    blood_bank=BloodBankProfile.objects.filter(user=request.user).first()
    if not BloodBankInventory.objects.filter(blood_bank=blood_bank).exists():
        BloodBankInventory(blood_bank=blood_bank,a_plus_in_cc=0,a_minus_in_cc=0,b_plus_in_cc=0,b_minus_in_cc=0,o_plus_in_cc=0,o_minus_in_cc=0,ab_plus_in_cc=0,ab_minus_in_cc=0).save()
    inventory = BloodBankInventory.objects.filter(blood_bank=blood_bank).first()
    return render(request,'blood_banks/my_inventory.html',{'inventory':inventory})

@login_required
@user_passes_test(test_func=check_blood_banks,login_url='/accounts/blood_banks_login')
def update_inventory(request):
    if request.method == 'POST':
        blood_bank=BloodBankProfile.objects.filter(user=request.user).first()
        inventory = BloodBankInventory.objects.filter(blood_bank=blood_bank).first()
        inventory.a_plus_in_cc = request.POST['a_plus_in_cc']
        inventory.a_minus_in_cc = request.POST['a_minus_in_cc']
        inventory.b_plus_in_cc = request.POST['b_plus_in_cc']
        inventory.b_minus_in_cc = request.POST['b_minus_in_cc']
        inventory.o_plus_in_cc = request.POST['o_plus_in_cc']
        inventory.o_minus_in_cc = request.POST['o_minus_in_cc']
        inventory.ab_plus_in_cc = request.POST['ab_plus_in_cc']
        inventory.ab_minus_in_cc = request.POST['ab_minus_in_cc']
        inventory.save()
        return redirect('my_inventory')
    else:
        blood_bank=BloodBankProfile.objects.filter(user=request.user).first()
        inventory = BloodBankInventory.objects.filter(blood_bank=blood_bank).first()
        return render(request,'blood_banks/update_inventory.html',{'inventory':inventory})

@login_required
@user_passes_test(test_func=check_blood_banks,login_url='/accounts/blood_banks_login')
def view_blood_requests(request):
    blood_bank=BloodBankProfile.objects.filter(user=request.user).first()
    blood_requests = BloodRequestBloodBank.objects.filter(blood_bank_profile=blood_bank).all()
    return render(request,'blood_banks/view_blood_requests.html',{'blood_requests':blood_requests})

@login_required
@user_passes_test(test_func=check_blood_banks,login_url='/accounts/blood_banks_login')
def accept_blood_request(request,request_id):
    blood_bank=BloodBankProfile.objects.filter(user=request.user).first()
    blood_request = BloodRequestBloodBank.objects.filter(blood_bank_profile=blood_bank,blood_request__request_id=request_id).first()
    blood_request.request_status = 'Accepted'
    blood_request.blood_bank_accepted_date_time = datetime.datetime.now()
    blood_request.save()
    return redirect('view_blood_requests_blood_banks')

@login_required
@user_passes_test(test_func=check_blood_banks,login_url='/accounts/blood_banks_login')
def get_bdb_data_blood_bank(request,request_id, blood_bank_id):
    blood_request = BloodRequest.objects.filter(request_id=request_id).first()
    blood_bank = BloodBankProfile.objects.filter(user__user_id=blood_bank_id).first()
    blood_request_blood_bank = BloodRequestBloodBank.objects.filter(blood_request=blood_request,blood_bank_profile=blood_bank).first()
    data = "transaction_id=" + blood_request_blood_bank.transaction_id
    response = requests.get("http://localhost:6000/bdb_read",data)
    return render(request,'blood_banks/get_bdb_data_blood_bank.html',{'response':response.json().get('asset').get('data')})

@login_required
@user_passes_test(test_func=check_blood_banks,login_url='/accounts/blood_banks_login')
def my_notifications(request):
    nots = Notification.objects.filter(user=request.user).all()
    return render(request,'blood_banks/my_notifications.html',{'nots':nots})