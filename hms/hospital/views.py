from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse
from django.utils import timezone



def homepage(request):
    return render(request, 'index.html')


def aboutpage(request):
    return render(request, 'about.html')

##Doctor creating their profile 
def createaccount(request):
    # initialize user
    user = "none"
    error = ""
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        repeatpassword = request.POST['repeatpassword']
        gender = request.POST['gender']
        phonenumber = request.POST['phonenumber']
        address = request.POST['address']
        birthdate = request.POST['dateofbirth']
        bloodgroup = request.POST['bloodgroup']

        try:
            if password == repeatpassword:
                # insert the values in the database
                Doctor.objects.create(name=name, email=email,
                                       gender=gender,
                                       phonenumber=phonenumber,
                                       address=address,
                                       birthdate=birthdate,
                                       bloodgroup=bloodgroup)

               
                user = User.objects.create_user(
                    first_name=name, email=email, password=password, username=email)
                
                doc_group = Group.objects.get(name='Doctor')
                # add the user to the patient group
                doc_group.user_set.add(user)
                # save the data in the user model
                user.save()
                error = 'no'
            else:
                error = 'yes'
        except Exception as e:
            #raise e
            error = 'yes'
    
    d = {'error': error}
    # print(error)
    return render(request, 'createaccount.html', d)



def loginpage(request):
    return render(request, 'login.html')



def loginpage(request):
    error = ""
    # authenticate takes three parameters ; request, username, password
    if request.method == 'POST':
     
        u = request.POST['email']
        p = request.POST['password']
        # print(u)
        # print(p)
        # this statement searches for the rows in the user model and saves them in the variable user
        user = authenticate(request, username=u, password=p)
        try:
            
            if user is not None:
                error = "no"
             
                login(request, user)

         
                g = request.user.groups.all()[0].name
                if g == 'Doctor':
                    d = {'error': error}
                    # return HttpResponse("Patient Logged in Successfully")
                    return render(request, 'patienthome.html', d)
    
        except Exception as e:
            error = "yes"
            print(e)
            # raise e
    return render(request, 'login.html')


def Logout(request):
    logout(request)
    return redirect('loginpage')

def Home(request):
   
    if not request.user.is_active:
        return redirect('loginpage')

    
    g = request.user.groups.all()[0].name
    if g == 'Doctor':
        return render(request, 'patienthome.html')


def profile(request):
    
    if not request.user.is_active:
        return redirect('loginpage')

    
    g = request.user.groups.all()[0].name
    if g == 'Doctor':

        patient_details = Patient.objects.all().filter(email=request.user)
        d = {'patient_details': patient_details}
        return render(request, 'patientprofile.html', d)


def MakeAppointments(request):
    error = ""
    
    # get all the registered doctors
    alldoctors = Doctor.objects.all()
    d = {'alldoctors': alldoctors}
    
    if request.method == 'POST':
            temp = request.POST['doctoremail']
            doctoremail = temp.split()[0]
            doctorname = temp.split()[1]
            patientname = request.POST['patientname']
            patientemail = request.POST['patientemail']
            appointmentdate = request.POST['appointmentdate']
            appointmenttime = request.POST['appointmenttime']
            symptoms = request.POST['symptoms']
            try:
                Appointment.objects.create(doctorname=doctorname, doctoremail=doctoremail, patientname=patientname, patientemail=patientemail,
                                           appointmentdate=appointmentdate, appointmenttime=appointmenttime, symptoms=symptoms, status=True, prescription="")
                error = "no"
            except:
                error = "yes"
            e = {"error": error}
            return render(request, 'patientmakeappointments.html', e)
    elif request.method == 'GET':
            return render(request, 'patientmakeappointments.html', d)

## appointmennt management 
def viewappointments(request):
    if not request.user.is_active:
        return redirect('loginpage')
    # print(request.user)
    g = request.user.groups.all()[0].name
    if g == 'Doctor':
        # appointmentdate__gte -> greater than
       
        upcomming_appointments = Appointment.objects.filter(doctoremail = request.user, appointmentdate__gte = timezone.now(), status = True).order_by('appointmentdate')
        
        previous_appointments = Appointment.objects.filter(doctoremail = request.user, appointmentdate__lt = timezone.now()).order_by('-appointmentdate')| Appointment.objects.filter(patientemail = request.user, status = False).order_by('-appointmentdate')
 
        d = {"upcomming_appointments": upcomming_appointments,"previous_appointments": previous_appointments}
        return render(request, 'patientviewappointments.html', d)
