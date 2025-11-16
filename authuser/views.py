from django.shortcuts import render,redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import User
from django.http import HttpResponseRedirect
from settings.models import Sector
from django.contrib.auth import update_session_auth_hash


class LoginView(View):
    def get(self,request):
        if request.user.is_authenticated:
            messages.success(request,'Your Are Already Logged')
            return redirect('/')
        else:
            return render(request,'authuser/login.html',{})


    def post(self,request):
        if request.method=='POST':
            username=request.POST.get('username')
            password=request.POST.get('password')
            next_url=request.POST.get('next')

            if username and password:
                user=authenticate(request,username=username,password=password)
                if user:
                    if user.is_active:
                        login(request,user)
                        messages.success(request,'You Are Logged Now Successfully')
                        return redirect(next_url or '/')
                    
                    messages.error(request,'sorry this user not active')
                    return render(request,'authuser/login.html')
                
                messages.error(request,'sorry this user not found ,pls try agin')
                return render(request,'authuser/login.html')
            
            messages.error(request,'sorry there are not any data here ,pls try again')

            
            return render(request,'authuser/login.html',{})
        
class LogooutView(View):
    def post(self,request):
        logout(request)
        messages.success(request,'You Are LogOut !!!! ')
        return redirect('/')
    

@login_required    
def all_user(request):
    users=User.objects.all()
    context={
        'users':users
    }
    return render(request,'authuser/all_user.html',context)

@login_required
def deactive_user(request):
    if request.method == 'POST':
        id=request.POST.get('id')
        user=User.objects.get(id=id)
        user.is_active=False
        user.save()
        messages.success(request,'ok done')
        return redirect('authuser:all_user')
  
@login_required
def active_user(request):
    if request.method =='POST':
        id=request.POST.get('id')
        user=User.objects.get(id=id)
        user.is_active=True
        user.save()
        messages.success(request,'done')
        return redirect('authuser:all_user')
    
@login_required
def add_user(request):
    sectors=Sector.objects.all()
    context={
        'sectors':sectors
    }
    return render(request,'authuser/add_user.html',context)


@login_required
def save_user(request):
    if request.method =='POST':
        full_name=request.POST.get('full_name')
        phone=request.POST.get('phone')
        image=request.FILES.get('image')
        email=request.POST.get('email')
        job=request.POST.get('job')
        username=request.POST.get('username')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        active = True if request.POST.get('active') in ['on', 'true', '1'] else False
        sector_id=request.POST.get('sector')
        notes=request.POST.get('notes')

        if not User.objects.filter(username=username).exists():
            if  password1 == password2:
                user=User.objects.create(
                    username=username,
                    email=email,
                    phone=phone,
                    full_name=full_name,
                    job=job,
                    image=image,
                    sector_id=sector_id,
                    is_active=active,
                    is_staff=active


                )
                user.set_password(password1)
                user.save()
                messages.success(request,'yOU add new user successfully')
                return redirect('authuser:add_user')
            
            messages.error(request,'Sorry this password != password2')
            return redirect('authuser:add_user')
        

        messages.error(request,'sorry this username already found')
        return redirect('authuser:add_user.html')
    
@login_required  
def edit_user(request,id):
    user=User.objects.get(id=id)
    sectors=Sector.objects.all()

    if request.method =='POST':
        full_name=request.POST.get('full_name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        image=request.FILES.get('image')
       
        job=request.POST.get('job')
        username=request.POST.get('username')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        active = True if request.POST.get('active') in ['on', 'true', '1'] else False
        sector_id=request.POST.get('sector')
        notes=request.POST.get('notes')

        if  password1 != password2:
            messages.error(request,'sorry password !=password2')
            return redirect('authuser:edit_user',id=id)



        
        user.username=username
        user.full_name=full_name
        user.email=email
        user.phone=phone
        if image:
            user.image=image
        user.job=job
        user.is_active=active
        user.sector_id=sector_id
        user.notes=notes

        if password1:

            user.set_password(password1)
            user.save()
            update_session_auth_hash(request,user)
        else:
            user.save()
        messages.success(request,'You are edit successfully')
        return redirect('authuser:all_user')
    

            




    context={
        'user':user,
        'sectors':sectors
    }
    return render(request,'authuser/edit_user.html',context)

@login_required
def edit_profile(request):
    sectors=Sector.objects.all()
    user=request.user
    if request.method =='POST':
        full_name=request.POST.get('full_name')
        image=request.FILES.get('image')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        sector_id=request.POST.get('sector')

        user.full_name=full_name
        if image:
            user.image=image
        user.email=email
        user.phone=phone
        if sector_id:
            user.sector_id=sector_id

        user.save()
        messages.success(request,'You update you data successfully')
        return redirect('authuser:all_user')




    context={
        'sectors':sectors,
        'user':user
    }
    return render(request,'authuser/edit_profile.html',context)

   




