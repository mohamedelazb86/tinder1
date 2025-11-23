from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import CashBox,CashTransaction,Category
from authuser.models import User
from django.http import HttpResponseRedirect
from django.contrib import messages
from . import models
from django.db.models import Sum
from datetime import datetime



@login_required
def all_cashbox(request):
    all_cashbox=CashBox.objects.all()
    context={
        'all_cashbox':all_cashbox
    }
    return render(request,'accounting/all_cashbox.html',context)

@login_required
def add_cashbox(request):
    users=User.objects.all()
    if request.method =='POST':
        name=request.POST.get('name')
        type=request.POST.get('type')
        is_main=True if request.POST.get('is_main') == 'on' else False
        is_active=True if request.POST.get('is_active') == 'on' else False
        treasurer_id=request.POST.get('treasurer')
        details=request.POST.get('details')

        CashBox.objects.create(
            name=name,
            type=type,
            is_main=is_main,
            is_active=is_active,
            treasurer_id=treasurer_id,
            details=details
        )
        messages.success(request,'مبرروك تم الحفظ بنجاح تحياتى')
        return redirect('accounting:all_cashbox')

    context={
        'users':users
    }
    return render(request,'accounting/add_cashbox.html',context)


@login_required
def edit_cashbox(request,id):
    cashbox=CashBox.objects.get(id=id)
    users=User.objects.all()
    if request.method == 'POST':
        name=request.POST.get('name')
        type=request.POST.get('type')
        is_main=True if request.POST.get('is_main') == 'on' else False
        is_active=True if request.POST.get('is_active') == 'on' else False
        treasurer_id=request.POST.get('treasurer')
        details=request.POST.get('details')

        cashbox.name=name
        cashbox.type=type
        cashbox.is_active=is_active
        cashbox.is_main=is_main
        cashbox.treasurer_id=treasurer_id
        cashbox.details=details
        cashbox.save()

        return redirect('accounting:all_cashbox')


    context={
        'cashbox':cashbox,
        'users':users
    }


    return render(request,'accounting/edit_cashbox.html',context)

@login_required
def active_cashbox(request):
    
    if request.method == 'POST':
        cashbox_id=request.POST.get('id')
        cashbox=CashBox.objects.get(id=cashbox_id)
        cashbox.is_active=True 
        cashbox.save()
        messages.success(request,'تم   التنشيط بنجاح ')

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def deactive(request):
    if request.method =='POST':
        cashbox_id=request.POST.get('id')
        cashbox=CashBox.objects.get(id=cashbox_id)
        cashbox.is_active=False
        cashbox.save()
        messages.success(request,'تم  إيقاف التنشيط بنجاح ')
        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    

@login_required
def transaction(request,id):

    cashbox=CashBox.objects.get(id=id)
    transactions=CashTransaction.objects.filter(cashbox=cashbox)

    total_income = transactions.aggregate(total=Sum('inbox'))['total'] or 0
    total_expenses = transactions.aggregate(total=Sum('absentminded'))['total'] or 0
    balance=total_income - total_expenses
    

    

    categories_in = Category.objects.filter(type='IN')
    categories_out = Category.objects.filter(type='OUT')

    context={
        'cashbox':cashbox,
        'transactions':transactions,
        'transactions':transactions,
        'categories_in':categories_in,
        'categories_out':categories_out,
        'total_income':total_income,
        'total_expenses':total_expenses,
        'balance':balance

    }

    return render(request,'accounting/transactions.html',context)

@login_required
def add_inbox(request):
     
     if request.method == 'POST':
        cashbox_id=request.POST.get('cashbox')
        amont=request.POST.get('amont')
        date=request.POST.get('date')
        try:
            date_parsed = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messages.error(request, "❌ من فضلك أدخل تاريخ صحيح بصيغة YYYY-MM-DD")
            return redirect(request.META.get('HTTP_REFERER'))
        no=request.POST.get('no')
        details=request.POST.get('details')
        category_id=request.POST.get('category')

        CashTransaction.objects.create(
            cashbox_id=cashbox_id,
            inbox=amont,
            date_transaction=date,
            no=no,
            details=details,
            category_id=category_id

        )

        messages.success(request,'تم إضافة المبلغ بنجاح')

  
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
     

@login_required
def add_absentminded(request):
    if request.method =='POST':
        cashbox_id=request.POST.get('cashbox')
        amont=float(request.POST.get('amont'))
        date=request.POST.get('date')
        try:
            date_parsed = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messages.error(request, "❌ من فضلك أدخل تاريخ صحيح بصيغة YYYY-MM-DD")
            return redirect(request.META.get('HTTP_REFERER'))
        
        transactions=CashTransaction.objects.filter(cashbox_id=cashbox_id)
        total_income=transactions.aggregate(total=Sum('inbox'))['total'] or 0
        total_expenses=transactions.aggregate(total=Sum('absentminded'))['total'] or 0
        total_balnce= total_income - total_expenses

        if amont > total_balnce :
            messages.error(request,f"❌ لا يمكن صرف مبلغ {amont} لأن رصيد الخزينة هو {total_balnce}")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


        no=request.POST.get('no')
        details=request.POST.get('details')
        category_id=request.POST.get('category')

        CashTransaction.objects.create(
            cashbox_id=cashbox_id,
            absentminded=amont,
            date_transaction=date,
            no=no,
            details=details,
            category_id=category_id

        )

        messages.success(request,'تم إضافة مصروف بنجاح')

  
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
     




    


  

    