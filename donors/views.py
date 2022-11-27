from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required,user_passes_test
from accounts.views import check_donors,get_coordinates
from django.db.models.functions import Radians, Power, Sin, Cos, ATan2, Sqrt, Radians
from django.db.models import F
import datetime,requests
from accounts.models import Notification
from blood_banks.models import BloodCamp,BloodCampEnrollment
from hospitals.models import BloodRequestDonor,BloodRequest
from .models import DonorProfile

@login_required
@user_passes_test(test_func=check_donors,login_url='/accounts/donors_login')
def add_profile(request):
    if request.method == 'POST':
        full_name=request.POST['full_name']
        gender=request.POST['gender']
        dob=request.POST['dob']
        blood_group=request.POST['blood_group']
        address=request.POST['address']
        area=request.POST['area']
        state=request.POST['state']
        city=request.POST['city']
        country=request.POST['country']
        zipcode=request.POST['zipcode']
        coords = get_coordinates(address, area , city, state, country)
        if coords is None:
            return render(request,'donors/add_profile.html')
        latitude=coords[0]
        longitude=coords[1]
        contact_email_address=request.POST['contact_email_address']
        contact_mobile_number=request.POST['contact_mobile_number']
        profile=DonorProfile(user=request.user,full_name=full_name,gender=gender,dob=dob,blood_group=blood_group,address=address,area=area,city=city,state=state,country=country,zipcode=zipcode,latitude=latitude,longitude=longitude,contact_email_address=contact_email_address,contact_mobile_number=contact_mobile_number,profile_pic=request.FILES['profile_pic'])
        profile.save()
        return redirect('view_donor_profile')
    else:
        return render(request,'donors/add_profile.html')

@login_required
@user_passes_test(test_func=check_donors,login_url='/accounts/donors_login')
def edit_profile(request):
    if request.method == "POST":
        profile=DonorProfile.objects.filter(user=request.user).first()
        profile.full_name=request.POST['full_name']
        profile.gender=request.POST['gender']
        profile.dob=request.POST['dob']
        profile.blood_group=request.POST['blood_group']
        profile.address=request.POST['address']
        profile.area=request.POST['area']
        profile.state=request.POST['state']
        profile.city=request.POST['city']
        profile.country=request.POST['country']
        profile.zipcode=request.POST['zipcode']
        coords = get_coordinates(request.POST['address'], request.POST['area'] ,request.POST['city'], request.POST['state'], request.POST['country'])
        profile.latitude=coords[0]
        profile.longitude=coords[1]
        profile.contact_email_address=request.POST['contact_email_address']
        profile.contact_mobile_number=request.POST['contact_mobile_number']
        profile.save()
        return redirect('view_donor_profile')
    else:
        profile=DonorProfile.objects.filter(user=request.user).first()
        return render(request,"donors/edit_profile.html",{'profile':profile})

@login_required
@user_passes_test(test_func=check_donors,login_url='/accounts/donors_login')
def view_profile(request):
    profile=DonorProfile.objects.filter(user=request.user).first()
    return render(request,"donors/view_profile.html",{'profile':profile})

@login_required
@user_passes_test(test_func=check_donors,login_url='/accounts/donors_login')
def see_camps_donors(request):
    profile=DonorProfile.objects.filter(user=request.user).first()
    dlat = Radians(F('latitude') - profile.latitude)
    dlong = Radians(F('longitude') - profile.longitude)
    a = (Power(Sin(dlat/2), 2) + Cos(Radians(profile.latitude)) * Cos(Radians(F('latitude'))) * Power(Sin(dlong/2), 2))
    c = 2 * ATan2(Sqrt(a), Sqrt(1-a))
    d = 6371 * c
    blood_camps = BloodCamp.objects.annotate(distance=d).order_by('distance').filter(distance__lt=10)
    return render(request,'donors/see_camps_donors.html',{'blood_camps':blood_camps})

@login_required
@user_passes_test(test_func=check_donors,login_url='/accounts/donors_login')
def enroll_in_camp(request,camp_id):
    blood_camp = BloodCamp.objects.filter(camp_id=camp_id).first()
    profile=DonorProfile.objects.filter(user=request.user).first()
    BloodCampEnrollment(blood_camp=blood_camp,donor_profile=profile).save()
    return redirect('enrolled_camps')

@login_required
@user_passes_test(test_func=check_donors,login_url='/accounts/donors_login')
def enrolled_camps(request):
    profile=DonorProfile.objects.filter(user=request.user).first()
    blood_camp_enrollments = BloodCampEnrollment.objects.filter(donor_profile=profile).all()
    return render(request,'donors/enrolled_camps.html',{'blood_camp_enrollments':blood_camp_enrollments})

@login_required
@user_passes_test(test_func=check_donors,login_url='/accounts/donors_login')
def view_blood_requests(request):
    profile=DonorProfile.objects.filter(user=request.user).first()
    blood_requests = BloodRequestDonor.objects.filter(donor_profile=profile).all()
    return render(request,'donors/view_blood_requests.html',{'blood_requests':blood_requests})

@login_required
@user_passes_test(test_func=check_donors,login_url='/accounts/donors_login')
def accept_blood_request(request,request_id):
    profile=DonorProfile.objects.filter(user=request.user).first()
    blood_request = BloodRequestDonor.objects.filter(donor_profile=profile,blood_request__request_id=request_id).first()
    blood_request.request_status = 'Accepted'
    blood_request.donor_accepted_date_time = datetime.datetime.now()
    blood_request.save()
    return redirect('view_blood_requests_donors')

@login_required
@user_passes_test(test_func=check_donors,login_url='/accounts/donors_login')
def get_bdb_data_donors(request,request_id):
    blood_request = BloodRequest.objects.filter(request_id=request_id).first()
    profile=DonorProfile.objects.filter(user=request.user).first()
    blood_request_donor = BloodRequestDonor.objects.filter(blood_request=blood_request,donor_profile=profile).first()
    data = "transaction_id=" + blood_request_donor.transaction_id
    response = requests.get("http://localhost:6000/bdb_read",data)
    return render(request,'donors/get_bdb_data_donors.html',{'response':response.json().get('asset').get('data')})

@login_required
@user_passes_test(test_func=check_donors,login_url='/accounts/donors_login')
def my_notifications(request):
    nots = Notification.objects.filter(user=request.user).all()
    return render(request,'donors/my_notifications.html',{'nots':nots})