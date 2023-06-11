from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from app1.models import *
from django.contrib import messages

from django.core.mail import send_mail
from django.conf import settings
from .helper import send_forget_password_mail
import random
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    return render(request,'index.html')


def all_login(request):
    if not request.user.is_anonymous:
        
        if request.session['remember']=='1':
            user=request.user
            if user.is_User:
                login(request,user)
                return redirect('user_page')
            elif user.is_sp:
                login(request,user)
                return redirect("sp_dash_main")
            elif user.is_admin:
                return render(request,"dashboard.html")
    if request.method=="POST":
        name=request.POST.get('email')
        pass1=request.POST.get('pas1')
        

        print(name ,pass1)
        # remember=request.POST['rem']/
        remember=request.POST.get('remember')
        print(remember)
        if remember:
            request.session['remember']='1'
        else:
            request.session['remember']='0'
        user=authenticate(username=name,password=pass1)
        print(user)
        if user is not None:
            if user.is_admin:
                # request.session['messege']='admin'
                login(request,user)
                user=request.user
                p=User.objects.filter(username=user)
                return render(request,"dashboard.html")
            elif user.is_sp:
                # request.session['messege']='s_p'
                login(request,user)
                return redirect("sp_dash_main")
                
            elif user.is_User:
                # request.session['messege']='user'
                # p=User.objects.filter(username=user)
                login(request,user)
                user=request.user
                return render(request,"main_user.html",{'names':user})
            else:
                return render(request,"user.html")
        else:
            messages.success(request,"please enter correct email and password")
            return render(request,'login.html') 
    
    return render(request,'login.html')

def user_register(request):
    if request.method =="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        ph_no=request.POST.get("ph_no")
        pas1=request.POST.get("pas1")
        pas2=request.POST.get("pas2")
        s=User.objects.filter(username=email)
        if s:
            messages.success(request,"you are already registered")
            return render(request,"user_register.html")
        else:
            if pas1==pas2:
                check=User.objects.create_user(email,email,pas1)
                check.save()
                check.first_name=name

                check.is_User=True
                check.save()
                user = User.objects.get(username=email)
                s=Coustmer(username=user,email=email,ph_no=ph_no,pas1=pas1,name=name)
                s.save()
                print(check.is_admin)
                # messages.success(request,"you are Registered successfully")
                return render(request,"login.html")
        return redirect("user_register")
    return render(request,"user_register.html")

def sp_register(request):
    if request.method=="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        pas1=request.POST.get("pas1")
        pas2=request.POST.get("pas2")
        ph_no=request.POST.get("ph_no")
        service=request.POST.get('service')
        img=request.FILES['img1']
        ad=request.POST.get("address")
        print(name)
        s=User.objects.filter(username=email)
        if s:
            messages.success(request,"you are already registered")
            return render(request,"sp_register.html")
        else:
            if pas1==pas2:
                check=User.objects.create_user(email,email,pas1)
                check.save()
                check.first_name=name
                check.is_sp=True
                check.save()
                user=User.objects.get(username=email)
                s=Vendor(vendorname=user,name=name,email=email,pas1=pas1,services=service,ph_no=ph_no,image=img,address=ad)
                s.save()
                print(check.is_sp)
                messages.success(request,"you are Registered successfully")
                return redirect(all_login)
            # return redirect("sp_register")
    return render(request,"sp_register.html")

def reset_password(request):
   
    if request.method=="POST":
        btn=request.POST.get('btn')
        if btn=='1':
            request.session["a"]=str(random.randrange(1000,9999))
            print(request.session["a"])
            
        if btn=='1':
                mail=request.POST.get('mail')
                print(mail)
                is_exists=User.objects.filter(email=mail)
                request.session['email']=mail
                if is_exists:
                    subject="Home_e| OTP"
    
                    message =f"hi your one time password is:"+request.session['a']
                    email_from =settings.EMAIL_HOST_USER
                    recipient_list=[mail]
                    send_mail(subject,message,email_from,recipient_list)
                    return render(request,'reset_password.html',{'type':2})
                else:
                    messages.success(request,"email not exists ")
                    return render(request,'reset_password.html',{'type':1}) 
        elif btn=='2':
                otp=request.POST.get('otp')
                print(otp)
                a=request.session['a']
                
                if otp==a:
                  return render(request,'reset_password.html',{'type':3})  
                else:
                    messages.success(request,"please enter the correct otp")
                    return render(request,'reset_password.html',{'type':2}) 
        else:
               pas=request.POST.get('pas')
               cpas=request.POST.get('cpas')
               if pas==cpas:
                    mail=request.session['email']
                    user=User.objects.get(username=mail)
                    user.set_password(pas)
                    user.save()
                    return redirect("login")
               else:
                    messages.success(request,"enter the password correctly")
                    return render(request,'reset_password.html',{'type':3}) 
    return render(request,'reset_password.html',{'type':1})
    # if request.method=="POST":
    #     email=request.POST['email']
    #     print(email)
    #     subject="your password reset link"
    #     message =f"hi,click here to change   by team Logway"
    #     email_from =settings.EMAIL_HOST_USER
    #     recipient_list=[email]
    #     send_mail(subject,message,email_from,recipient_list)
    #     return render(request,'index.html')
    return render(request,"reset_password.html")
# @login_required
def pumber_service(request):
    sp=Vendor.objects.filter(confirm=True,services='plumber')
    count=sp.count()
    if request.user.is_anonymous:
        nav=0
    else:
        nav=1
    return render(request,"new_service_provider.html",{"sp":sp,"count":count,"nav":nav})    


def user_page(request):
    user=request.user
    return render(request,"main_user.html")


def log_out(request):
    logout(request)
    return render(request,'index.html')

def admin_user_dash(request):
    user=Coustmer.objects.all()
    return render(request,'admin_user_dash.html',{"user":user})

def dashboard(request):
    u=Coustmer.objects.all()
    s=Vendor.objects.all()
    c_count=u.count
    v_count=s.count
    return render(request,'dashboard.html',{"c_count":c_count,"v_count":v_count})

def admin_home(request):
    u=Coustmer.objects.all()
    s=Vendor.objects.all()
    c_count=u.count
    v_count=s.count

    return  render(request,"admin_home.html",{"c_count":c_count,"v_count":v_count})

def admin_vendor_delete(request):
    #      if request.method=="POST":
    #           action=Vendor.objects.get()
    #           buton=request.POST.get('button')
    #       if buton=="confirm":
    #            action.confirm=True
    #            action.save()
    #            ven=Vendor.objects.filter(confirm=False)
    #            ven=ven.all().values()
    #            ven1={'ven':ven,'nav':3}
    #            return render(request,"vconfirm.html",ven1)
    #       else:
    #            name=action.email
    #            user=User.objects.get(username=name)
    #            user.delete()
    #            action.delete()
    #            ven=Vendor.objects.filter(confirm=False)
    #            ven=ven.all().values()
    #            ven1={'ven':ven,}
    #            return render(request,"vconfirm.html",ven1)
    #  ven=Vendor.objects.filter(confirm=False)
    #  ven=ven.all().values()
    #  ven1={'ven':ven}
    #  return render(request,"vconfirm.html",ven1)
    ven=Vendor.objects.all()
    return render(request,'admin_vendor_delete.html',{"ven":ven})
def vendor_delete(request,pk):
        if request.method=="POST":
            action=Vendor.objects.get(id=pk)
            # buton=request.POST.get('button')
            # if buton:
            name=action.email
            user=User.objects.get(username=name)
            user.delete()
            action.delete()
            ven=Vendor.objects.all()
            return render(request,"admin_vendor_delete.html",{"ven":ven})
        return render(request,"admin_vendor_delete.html",{"ven":ven})


def vaction(request,pk):
     if request.method=="POST":
          action=Vendor.objects.get(id=pk)
          buton=request.POST.get('button')
          if buton=="confirm":
               action.confirm=True
               action.save()
               ven=Vendor.objects.filter(confirm=False)
               ven=ven.all().values()
               ven1={'ven':ven,'nav':3}
               return render(request,"vconfirm.html",ven1)
          else:
               name=action.email
               user=User.objects.get(username=name)
               user.delete()
               action.delete()
               ven=Vendor.objects.filter(confirm=False)
               ven=ven.all().values()
               ven1={'ven':ven,}
               return render(request,"vconfirm.html",ven1)
     ven=Vendor.objects.filter(confirm=False)
     ven=ven.all().values()
     ven1={'ven':ven}
     return render(request,"vconfirm.html",ven1)


def vconfirm(request):
     if request.method=="POST":
          action=Vendor.objects.get()
          buton=request.POST.get('button')
          if buton=="confirm":
               action.confirm=True
               action.save()
               ven=Vendor.objects.filter(confirm=False)
               ven=ven.all().values()
               ven1={'ven':ven,'nav':3}
               return render(request,"vconfirm.html",ven1)
          else:
               name=action.email
               user=User.objects.get(username=name)
               user.delete()
               action.delete()
               ven=Vendor.objects.filter(confirm=False)
               ven=ven.all().values()
               ven1={'ven':ven,}
               return render(request,"vconfirm.html",ven1)
     ven=Vendor.objects.filter(confirm=False)
     ven=ven.all().values()
     ven1={'ven':ven}
     return render(request,"vconfirm.html",ven1)

def admin_bookings(request):
    b=Bookings.objects.all()
    return render(request,"admin_bookings.html",{"booking":b})

def service_provider_login(request):
    sp=Vendor.objects.filter(confirm=True,services='plumber')
    return render(request,"service_dashboard.html",{"sp":sp})

def service_bookings(request,pk):
    if request.user.is_anonymous:
        # messages.success("please login to book the service")
        return redirect('login')
    else:
        print(request.user)
        if request.method=="POST":
            user_name=request.POST.get("name")
            user_ph=request.POST.get("ph_no")
            user_add=request.POST.get("address")
            user_email=request.POST.get("email")
            user_time=request.POST.get("time")
            user_date=request.POST.get("date")
            sp=Vendor.objects.get(id=pk)
            service=sp.services
            print(service)
            vendorname=sp.vendorname
            user=request.user
            user_name=user.first_name
            print(user.first_name)
            service_type=sp.services
            customer = Coustmer.objects.get(username=user)
            a_b=Bookings.objects.filter(user_email=customer,
                        Vendor_name=sp,
                        service_type=service_type)
            if a_b:
                messages.warning(request,"you already booked this service the service provider will accept your service see the bookings")
                if service=="plumber":
                    return redirect("pumber_service")
                elif service=="Electrision":
                    return redirect("elecrision")
            else:

                b=Bookings(user_email=customer,
                        Vendor_name=sp,
                        user_ph=user_ph,
                        user_add=user_add,
                        user_date=user_date,
                        user_time= user_time,
                        user_name=user_name,
                        service_type=service_type)
                b.save()
                # sending messege  to the service_provoider
                subject="Home_e| service is booked"
                print(vendorname)
                message =f"You got a service order from {str(customer.username)} from {user_add}"
                email_from =settings.EMAIL_HOST_USER
                recipient_list=[vendorname]
                send_mail(subject,message,email_from,recipient_list)

        sp=Vendor.objects.filter(confirm=True,services='plumber')
        count=sp.count()
        return render(request,"new_service_provider.html",{"sp":sp,"count":count})
    
def booking_confirm(request,pk):
        if request.method=="POST":
            booking=Bookings.objects.get(id=pk)
            print(booking)
            booking.status="Accepted"
            booking.save()
            user=request.user
            sp=Vendor.objects.filter(vendorname=user)
            Booking=Bookings.objects.filter(Vendor_name__in=sp)
            
            if Booking:
                print("hello")
                print(Booking)
                return render(request,"sp_dash_bookings.html",{"booking":Booking})
        return render(request,"sp_dash_bookings.html")

def sp_dash_main(request):
    
    user=request.user
    sp=Vendor.objects.filter(vendorname=user)

    Booking=Bookings.objects.filter(Vendor_name__in=sp)
    t_count=Booking.count
    p_Booking=Bookings.objects.filter(Vendor_name__in=sp,status="pending")
    p_count=p_Booking.count
    a_Booking=Bookings.objects.filter(Vendor_name__in=sp,status="Accepted")
    a_count=a_Booking.count

    if not Booking:
        print("hello")
        print(Booking)
        return render(request,"sp_dash_main.html",{'sp':sp,})
    return render(request,"sp_dash_main.html",{'sp':sp,'t_count':t_count,'p_count':p_count,'a_count':a_count})
    

def sp_dash_bookings(request):
    if request.user.is_anonymous:
        # messages.success("please login to book the service")
        return redirect('login')
    else:
        user=request.user
        sp=Vendor.objects.filter(vendorname=user)
        Booking=Bookings.objects.filter(Vendor_name__in=sp)
                
        if Booking:
            print("hello")
            print(Booking)  
            return render(request,"sp_dash_bookings.html",{"booking":Booking})
    return render(request,"sp_dash_bookings.html")

def sp_dash_profile(request):
    user=request.user
    sp=Vendor.objects.filter(vendorname=user)
    return render(request,"sp_dash_profile.html",{"sp":sp})

def sp_dash_profile_edit(request,pk):
    if request.method=='POST':
        name=request.POST.get("name")
        ph_no=request.POST.get("ph_no")
        address=request.POST.get("address")
        image=request.FILES['image']
        sp=Vendor.objects.get(id=pk)
        sp.name=name
        sp.ph_no=ph_no
        sp.address=address
        sp.image=image
        sp.save()
        print(image,name,ph_no)
    return redirect(sp_dash_profile)

def elecrision(request):
    sp=Vendor.objects.filter(confirm=True,services='Electrision')
    count=sp.count()
    return render(request,"elecrision.html",{"sp":sp,"count":count})
def user_profile(request):
    return render(request,"user_profile.html")

def user_bookings(request):
    user=request.user
    c=Coustmer.objects.get(username=user)
    b=Bookings.objects.filter(user_email=c)
    print(b)
    return render(request,"user_bookings.html",{"booking":b})
    

