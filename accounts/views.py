from django.shortcuts import render,redirect
from django.contrib import auth
from django.conf import settings
import math,random,requests,json
from geopy.geocoders import Nominatim
from twilio.rest import Client
from .models import User

def check_admins(user):
    if user.user_type == 'Admin':
        return True
    else:
        return False

def check_hospitals(user):
    if user.user_type == 'Hospital':
        return True
    else:
        return False

def check_blood_banks(user):
    if user.user_type == 'Blood Bank':
        return True
    else:
        return False

def check_donors(user):
    if user.user_type == 'Donor':
        return True
    else:
        return False

def generateOTP():
    digits = "0123456789"
    OTP = ""
    for _ in range(6) : 
        OTP += digits[math.floor(random.random() * 10)]
    return OTP

def get_coordinates(address,area,city,state,country):
    geolocator = Nominatim(user_agent="healtrics")
    if address is not None:
        location = geolocator.geocode(address + "," + area + "," + city + "," + state + "," + country)
    else:
        location = geolocator.geocode(area + "," + city + "," + state + "," + country)
    if location is not None:
        return (location.latitude, location.longitude)
    location = geolocator.geocode(area + "," + city + "," + state + "," + country)
    if location is not None:
        return (location.latitude, location.longitude)
    location = geolocator.geocode(city + "," + state + "," + country)
    if location is not None:
        return (location.latitude, location.longitude)
    return None

def sendMail(subject,message,email_from,recipient_list):
    url = "http://localhost:5050/send_mail"
    querystring = {"subject":subject,"message":message,"email_from":email_from,"to_email":recipient_list[0]}
    response = requests.get(url=url,params=querystring)
    print(response.text)

def sendSMS(message,contact_number):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(from_=settings.TWILIO_PHONE_NUMBER,body =message,to =contact_number)
    print(message.sid)

def writeBDB(data):
    url = "http://localhost:6000/bdb_write"
    response = requests.get(url=url,params=data)
    return response.json().get('transaction_id')

def isSuitableDonorByType(request_type,blood_type):
    REQUEST_TYPE_MAP = {'Whole Blood':{"A+":["A+", "A-", "O+", "O-"], "A-":["A-", "O-"], "B+":["B+", "B-", "O+", "O-"], "B-":["B-", "O-"], "O+":["O+", "O-"], "O-":["O-"], "AB+":["A+","A-","B+","B-","O+","O-","AB+","AB-"], "AB-":["AB-", "A-", "B-", "O-"]},'Red Cells':["O+", "O-", "A-", "B-"],'Platelets':["A+", "A-", "B+", "O+", "AB+", "AB-"],'Plasma':["AB+", "AB-"]}
    if request_type == 'Whole Blood':
        return REQUEST_TYPE_MAP.get('Whole Blood').get(blood_type)
    return REQUEST_TYPE_MAP.get(request_type)

def getDonationUses(donation_type_needed):
    DONATION_USES = {'Whole Blood':"Whole blood is frequently given to trauma patients and people undergoing surgery.",'Red Cells':"Red cells from a Power Red donation are typically given to trauma patients, newborns and emergency transfusions during birth, people with sickle cell anemia, and anyone suffering blood loss.",'Platelets':" Platelets are a vital element of cancer treatments and organ transplant procedures, as well as other surgical procedures.",'Plasma':" AB Plasma is used in emergency and trauma situations to help stop bleeding."}
    return DONATION_USES.get(donation_type_needed)

def getApproxTimeForDonating(donation_type_needed):
    APPROX_DONATION_TIME = {'Whole Blood':"About 1 hour",'Red Cells':" About 1.5 hours",'Platelets':"About 2.5-3 hours",'Plasma':"About 1 hour and 15 minutes"}
    return APPROX_DONATION_TIME.get(donation_type_needed)

def admins_login(request):
    if request.method == 'POST':
        email_address = request.POST['email_address']
        password = request.POST['password']
        user = auth.authenticate(username=email_address,password=password)
        if user is not None and user.user_type=='Admin':
            auth.login(request,user,backend=None)
            return redirect('verify_hospitals')
        else:
            return redirect('admins_login')
    else:
        return render(request,'accounts/admins_login.html')

def hospitals_signup(request):
    if request.method == 'POST':
        email_address = request.POST['email_address']
        mobile_number = request.POST['mobile_number']
        password = request.POST['password']
        email_otp = generateOTP()
        mobile_otp = generateOTP()
        user = User(email_address=email_address, mobile_number=mobile_number, user_type='Hospital',email_code=email_otp, mobile_code=mobile_otp)
        user.set_password(password)
        user.save()
        sendMail("Healtrics Account Verification",email_otp,settings.EMAIL_HOST_USER,[email_address])
        sendSMS("Healtrics Account Verification : " + mobile_otp,mobile_number)
        auth.login(request,user,backend=None)
        return redirect('hospitals_verify')
    else:
        return render(request,'accounts/hospitals_signup.html')

def hospitals_verify(request):
    if request.method == 'POST':
        user = User.objects.filter(user_id=request.user.user_id).first()
        email_otp = request.POST['email_otp']
        mobile_otp = request.POST['mobile_otp']
        if user.email_code == email_otp and user.mobile_code == mobile_otp:
            user.is_email_verified = True
            user.is_mobile_verified = True
            user.save()
            return redirect('add_hospital_profile')
        else:
            return redirect('hospitals_verify')
    else:
        return render(request,'accounts/hospitals_verify.html')

def hospitals_login(request):
    if request.method == 'POST':
        email_address = request.POST['email_address']
        password = request.POST['password']
        user = auth.authenticate(username=email_address,password=password)
        if user is not None and user.user_type=='Hospital' and user.is_email_verified and user.is_mobile_verified:
            auth.login(request,user,backend=None)
            return redirect('view_hospital_profile')
        else:
            return redirect('hospitals_login')
    else:
        return render(request,'accounts/hospitals_login.html')

def blood_banks_signup(request):
    if request.method == 'POST':
        email_address = request.POST['email_address']
        mobile_number = request.POST['mobile_number']
        password = request.POST['password']
        email_otp = generateOTP()
        mobile_otp = generateOTP()
        user = User(email_address=email_address, mobile_number=mobile_number, user_type='Blood Bank',email_code=email_otp, mobile_code=mobile_otp)
        user.set_password(password)
        user.save()
        sendMail("Healtrics Account Verification",email_otp,settings.EMAIL_HOST_USER,[email_address])
        sendSMS("Healtrics Account Verification : " + mobile_otp,mobile_number)
        auth.login(request,user,backend=None)
        return redirect('blood_banks_verify')
    else:
        return render(request,'accounts/blood_banks_signup.html')

def blood_banks_verify(request):
    if request.method == 'POST':
        user = User.objects.filter(user_id=request.user.user_id).first()
        email_otp = request.POST['email_otp']
        mobile_otp = request.POST['mobile_otp']
        if user.email_code == email_otp and user.mobile_code == mobile_otp:
            user.is_email_verified = True
            user.is_mobile_verified = True
            user.save()
            return redirect('add_blood_bank_profile')
        else:
            return redirect('blood_banks_verify')
    else:
        return render(request,'accounts/blood_banks_verify.html')

def blood_banks_login(request):
    if request.method == 'POST':
        email_address = request.POST['email_address']
        password = request.POST['password']
        user = auth.authenticate(username=email_address,password=password)
        if user is not None and user.user_type=='Blood Bank' and user.is_email_verified and user.is_mobile_verified:
            auth.login(request,user,backend=None)
            return redirect('view_blood_bank_profile')
        else:
            return redirect('blood_banks_login')
    else:
        return render(request,'accounts/blood_banks_login.html')

def donors_signup(request):
    if request.method == 'POST':
        email_address = request.POST['email_address']
        mobile_number = request.POST['mobile_number']
        password = request.POST['password']
        email_otp = generateOTP()
        mobile_otp = generateOTP()
        user = User(email_address=email_address, mobile_number=mobile_number, user_type='Donor',email_code=email_otp, mobile_code=mobile_otp)
        user.set_password(password)
        user.save()
        sendMail("Healtrics Account Verification",email_otp,settings.EMAIL_HOST_USER,[email_address])
        sendSMS("Healtrics Account Verification : " + mobile_otp,mobile_number)
        auth.login(request,user,backend=None)
        return redirect('donors_verify')
    else:
        return render(request,'accounts/donors_signup.html')

def donors_verify(request):
    if request.method == 'POST':
        user = User.objects.filter(user_id=request.user.user_id).first()
        email_otp = request.POST['email_otp']
        mobile_otp = request.POST['mobile_otp']
        if user.email_code == email_otp and user.mobile_code == mobile_otp:
            user.is_email_verified = True
            user.is_mobile_verified = True
            user.save()
            return redirect('add_donor_profile')
        else:
            return redirect('donors_verify')
    else:
        return render(request,'accounts/donors_verify.html')

def donors_login(request):
    if request.method == 'POST':
        email_address = request.POST['email_address']
        password = request.POST['password']
        user = auth.authenticate(username=email_address,password=password)
        if user is not None and user.user_type=='Donor' and user.is_email_verified and user.is_mobile_verified:
            auth.login(request,user,backend=None)
            return redirect('view_donor_profile')
        else:
            return redirect('donors_login')
    else:
        return render(request,'accounts/donors_login.html')

def logout(request):
    auth.logout(request)
    return redirect('home1')