from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import CashBox,CashTransaction
from authuser.models import User
from django.http import HttpResponseRedirect
from django.contrib import messages
from . import models



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
    
# @login_required   
# def all_transaction(request):
#     cashboxs=CashBox.objects.filter(treasurer=request.user)
#     transactions=CashTransaction.objects.filter(cashbox__in=cashboxs)

#     context={
#         'transactions':transactions
#     }
#     return render(request,'accounting/all_transaction.html',context)

from django.db.models import Sum
@login_required
def all_transaction(request):

    cashboxs = CashBox.objects.filter(treasurer=request.user)

    selected_id = request.GET.get('cashbox')

    if selected_id:
        transactions = CashTransaction.objects.filter(cashbox_id=selected_id)
    else:
        transactions = CashTransaction.objects.filter(cashbox__in=cashboxs)

    # حسابات الإيرادات والمصروفات
    total_income = transactions.aggregate(total=Sum('inbox'))['total'] or 0
    total_expenses = transactions.aggregate(total=Sum('absentminded'))['total'] or 0
    total_balance = total_income - total_expenses

    context = {
        'transactions': transactions,
        'cashboxs': cashboxs,
        'selected_id': selected_id,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'total_balance': total_balance,
    }

    return render(request, 'accounting/all_transaction.html', context)

@login_required
def search(request):

    cashboxs = CashBox.objects.filter(treasurer=request.user)

    selected_id = request.GET.get('cashbox')

    # الخط الأساسي: فلترة على الخزينة
    if selected_id:
        transactions = CashTransaction.objects.filter(cashbox_id=selected_id)
    else:
        transactions = CashTransaction.objects.filter(cashbox__in=cashboxs)

    # فلترة التاريخ
    date1 = request.GET.get('date1')
    date2 = request.GET.get('date2')

    if date1 and date2:
        # نتأكد أن التاريخ صحيح
        if date1 <= date2:
            transactions = transactions.filter(date_transaction__range=[date1, date2])

    context = {
        'transactions': transactions,
        'cashboxs': cashboxs,
        'selected_id': selected_id,
    }

    return render(request, 'accounting/all_transaction.html', context)


