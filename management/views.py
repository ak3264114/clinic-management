from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout ,login ,authenticate
from blog.models import Blog

from management.models import Appointment, Doctor, Patient


def home(request): 
    if request.user.is_staff :
        data = Doctor.objects.filter(user = request.user)
        doctors = Doctor.objects.all
        return render(request, 'index.html', {'data': data ,'doctors': doctors })
        # return redirect('add_details')
        # user_id = request.user.id
        # data = Doctor.objects.get(pk=user_id)
        # return render(request, 'profile.html', {'data': data})
    elif request.user.is_authenticated:
        if  Patient.objects.filter(user = request.user).exists():
            data = Patient.objects.get(user = request.user)
            doctors = Doctor.objects.all
            return render(request, 'index.html', {'data': data,'doctors': doctors })
        else:
            return render(request, 'index.html')
    # elif request.user.is_authenticated:
        
    #     data = Patient.objects.get(user = request.user)
    #     doctors = Doctor.objects.all
    #     return render(request, 'index.html', {'data': data,'doctors': doctors })
    else:
        doctors = Doctor.objects.all
        return render(request, 'index.html', { 'doctors': doctors})      

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['first_name']
        lname = request.POST['last_name']
        email = request.POST['email']
        user_type = request.POST['user_type']
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']
        
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('signup')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('signup')
        
        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('signup')
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('signup')
        
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('signup')
        if user_type == "patient" and pass1 == pass2:
            myuser = User.objects.create_user(username, email, pass1)
            myuser.first_name = fname
            myuser.last_name = lname
            Patient.first_name = fname
            Patient.last_name = lname
            myuser.is_active = True
            myuser.save()
            messages.success(request, "Your Account has been created succesfully!! Please Signin")
            return redirect('signup')
        if user_type == "doctor" and pass1 == pass2:
            myuser = User.objects.create_user(username, email, pass1)
            Doctor.first_name = fname
            Doctor.last_name = lname
            myuser.first_name = fname
            myuser.last_name = lname
            # myuser.is_active = False
            myuser.is_staff = True
            myuser.save()
            messages.success(request, "Your Account has been created succesfully!!Please Signin")
            return redirect('home')
        else:
            return HttpResponse("An error occourse!! Please try again")   
    else:
         return render(request, 'signup.html')

def signin(request):
    if request.method =="POST":
        username = request.POST['username']
        password = request.POST['password1']
        user = authenticate(username = username , password=password)
        
        if user is not None:
            login(request, user)
            return redirect ('profile')
        # elif User.is_authenticated:
        #     return HttpResponse('You have already sign in')         
        else:
            messages.error(request, "wrong credentials")
            return redirect ("signin")
           
    return render(request, 'signin.html')
    


def signout(request):
    logout(request)
    return redirect("home")

def details_doctors(request):
    return HttpResponse(request.user.id)

def doctors_dashboard(request):
    pass

def profile(request):
    if request.user.is_staff :
        if  Doctor.objects.filter(user = request.user).exists():
            if Blog.objects.filter(blog_author = request.user).exists():
                data = Doctor.objects.get(user = request.user)
                appointment=Appointment.objects.filter(booked_for_dr_name= request.user.Doctor.id)
                contents = Blog.objects.filter(blog_author = request.user)
                return render(request, 'profile.html', {'data': data , 'contents':contents, 'appointment':appointment})
            else:
                data = Doctor.objects.get(user = request.user)
                contents = Blog.objects.filter(blog_author = request.user)
                return render(request, 'profile.html', {'data': data})
        else:
            return redirect('add_details')
        # user_id = request.user.id
        # data = Doctor.objects.get(pk=user_id)
        # return render(request, 'profile.html', {'data': data})
    elif request.user.is_authenticated:
        if  Patient.objects.filter(user = request.user).exists():
            data = Patient.objects.get(user = request.user)
            appointment=Appointment.objects.filter(booked_by_name =request.user)

            return render(request, 'profile.html', {'data': data, 'appointment':appointment})
        else:
            return redirect('add_details')

    else:
        return render(request, 'index.html')

def add_details(request):
    if request.user.is_authenticated:
        if request.method =='POST' and request.user.is_staff:
            user = request.user.id
            image =request.FILES['image']
            first_name = request.user.first_name
            last_name = request.user.last_name
            qualification_higest = request.POST['qualification_higest']
            specilization = request.POST['specilization']
            about = request.POST['about']
            phone_no = request.POST['phone_no']
            add_line_1 = request.POST['add_line_1']
            add_city = request.POST['add_city']
            add_state = request.POST['add_state']
            add_Pincode = request.POST['add_Pincode']
            if len(phone_no)!=10:
                messages.error(request, "Phone no. must be 10 digits!!")
                return redirect('add_details')
            if len(add_Pincode)!=6:
                messages.error(request, "Pin Code must be 6 digits!!")
                return redirect('add_details')
            Doctor(first_name=first_name, last_name=last_name, user_id=user, image= image , qualification_higest=qualification_higest, specilization=specilization, about=about, phone_no=phone_no, add_line_1=add_line_1, add_city=add_city, add_state=add_state, add_Pincode=add_Pincode).save()
            messages.success(request, "Your details has been added succesfully!")
            return redirect('add_details')

        elif request.method =='POST':
            user = request.user.id
            first_name = request.user.first_name
            last_name = request.user.last_name
            image = request.FILES['image']
            phone_no = request.POST['phone_no']
            add_line_1 = request.POST['add_line_1']
            add_city = request.POST['add_city']
            add_state = request.POST['add_state']
            add_Pincode = request.POST['add_Pincode']
            
            Patient(first_name=first_name, last_name=last_name , user_id=user, image=image, phone_no=phone_no, add_line_1=add_line_1, add_city=add_city, add_state=add_state, add_Pincode=add_Pincode).save()
            messages.success(request, "Your details has been added succesfully!")
            return redirect('add_details')

        elif request.method =='GET':
            return render (request, 'add-details.html')

        else:
            return HttpResponse("An error occoured!!! Please try again")

    else:
        return render(request,'index.html')


def edit_details(request):
    if request.user.is_staff :
        data = Doctor.objects.get(user = request.user)
        return render(request, 'edit-profile.html', {'profile_data': data})
    elif request.user.is_authenticated:
        data = Patient.objects.get(user = request.user)
        return render(request, 'edit-profile.html', {'profile_data': data})
    else:
        redirect('profile')

def update(request):
    if request.user.is_authenticated:
        if request.method =='POST' and request.user.is_staff:
            uptd_profile = Doctor.objects.filter(user=request.user)
            uptd_profile.first_name = request.POST.get('first_name')
            uptd_profile.last_name = request.POST.get('last_name')
            uptd_profile.qualification_higest = request.POST.get('qualification_higest')
            uptd_profile.specilization = request.POST.get('specilization')
            uptd_profile.phone_no = request.POST.get('phone_no')
            uptd_profile.add_line_1 = request.POST.get('add_line_1')
            uptd_profile.add_city = request.POST.get('add_city')
            uptd_profile.add_state = request.POST.get('add_state')
            uptd_profile.add_Pincode = request.POST.get('add_Pincode')
            uptd_profile.save()
            messages.success(request, "Your details has been Updated succesfully!")
            return redirect('edit_details')
        elif request.method =='POST':
            uptd_profile = Patient.objects.filter(user=request.user)
            uptd_profile.first_name = request.POST.get('first_name')
            uptd_profile.last_name = request.POST.get('last_name')
            uptd_profile.phone_no = request.POST.get('phone_no')
            uptd_profile.add_line_1 = request.POST.get('add_line_1')
            uptd_profile.add_city = request.POST.get('add_city')
            uptd_profile.add_state = request.POST.get('add_state')
            uptd_profile.add_Pincode = request.POST.get('add_Pincode')
            uptd_profile.save()
            messages.success(request, "Your details has been Updated succesfully!")
            return redirect('edit_details')
        else:
            return HttpResponse(request,"an error occoured!")

def book_appointment(request,doctor_id):
    if request.method=='POST':
        booked_by_name=User.objects.get(id=request.user.id)
        booked_for_dr_name =Doctor.objects.get(id=doctor_id)
        date = request.POST['date']
        time = request.POST['time']
        phone_number = request.POST['phone_number']
        speciality = request.POST['speciality']
        Appointment(booked_by_name=booked_by_name,booked_for_dr_name=booked_for_dr_name , date=date, time=time, phone_number=phone_number, speciality=speciality).save() 
        return HttpResponse("Done")     
    if request.method=='GET':
        if request.user.is_staff :
            data = Doctor.objects.filter(user = request.user)
            doctor_details = Doctor.objects.get(pk=doctor_id)
            return render(request, 'book-appointment.html', {'data': data,'doctor_details':doctor_details})
        elif request.user.is_authenticated:
            data = Patient.objects.get(user = request.user)
            doctor_details = Doctor.objects.get(pk=doctor_id)
            return render(request, 'book-appointment.html', {'data': data, 'doctor_details':doctor_details})
        else:
            return render(request, 'signup.html')
