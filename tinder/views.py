from django.shortcuts import render,redirect
from .models import Tinder,TinderFiles,TindetItem
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from contact.models import Company_by,Competitor,Category
from authuser.models import User
from django.http import HttpResponseRedirect


@login_required
def all_tinder(request):
    tinders=Tinder.objects.all()

    context={
        'tinders':tinders
    }
    return render(request,'tinder/all_tinder.html',context)

@login_required
def delete_tinder(request):
   
    if request.method =='POST':
        tinder_id=request.POST.get('id')
        tinder=Tinder.objects.get(id=tinder_id)
        tinder.delete()
        messages.success(request,f'You are delete {tinder.title} successfully')
        return redirect('tinder:all_tinder')
    
@login_required   
def edit_tinder(request,id):
    tinder=Tinder.objects.get(id=id)
    awared_by=Company_by.objects.all()
    competitor=Competitor.objects.all()
    users=User.objects.all()
    status_choices = Tinder._meta.get_field('status').choices  # ✅ هكذا نحصل على choices
    insurancetype = Tinder._meta.get_field('insurance_type').choices

    tinder_file=TinderFiles.objects.filter(tinder=tinder)
    tinder_item=TindetItem.objects.filter(tinder=tinder)

    if request.method =='POST':
        title=request.POST.get('title')
        descriptions=request.POST.get('descriptions')
        open_date=request.POST.get('open_date')
        close_date=request.POST.get('close_date')
        insurance_amount=request.POST.get('insurance_amount')
        insurance_type=request.POST.get('insurance_type')
        offer_value=request.POST.get('offer_value')
        company_by_id=request.POST.get('company_by')
        awared_by_id=request.POST.get('awared_byy')
        status=request.POST.get('status')
       
        
        

        tinder.title=title
        tinder.descriptions=descriptions
        tinder.created_by=request.user

        if close_date > open_date:
            tinder.open_date=open_date
            tinder.close_date=close_date

        tinder.insurance_amount=insurance_amount
        tinder.insurance_type=insurance_type
        tinder.offer_value=offer_value
        tinder.company_by_id=company_by_id or None
        if awared_by_id:
            tinder.awared_by_id=awared_by_id or None

        tinder.status=status
        
      
        tinder.save()

        
        # ⚡ نلف على كل العناصر اللي فيها file_title
        i = 0
        while True:
            title_key = f'file_list[{i}][file_title]'
            file_key = f'file_list[{i}][file_upload]'
            if title_key in request.POST and file_key in request.FILES:
                file_title = request.POST.get(title_key)
                file_obj = request.FILES.get(file_key)

                # تحقق أنه ملف PDF
                if file_obj.name.lower().endswith('.pdf'):
                    TinderFiles.objects.create(
                        tinder=tinder,
                        title=file_title,
                        files=file_obj
                    )
                else:
                    messages.warning(request, f"❌ الملف '{file_obj.name}' ليس PDF وتم تجاهله")

                i += 1
            else:
                break  # لما يخلص الملفات نخرج من اللوب
          
        ii = 0
        while True:
            item_key = f'items_list[{ii}][item]'
            quantity_key = f'items_list[{ii}][quantity]'
            suplyprice_key = f'items_list[{ii}][supply_price]'
            code_key = f'items_list[{ii}][code]'
            tinderprice_key = f'items_list[{ii}][tinder_price]'
            unit_key = f'items_list[{ii}][unit]'
            if item_key in request.POST and suplyprice_key in request.POST  and  unit_key in request.POST and quantity_key in request.POST and  code_key in request.POST:
                item_title = request.POST.get(item_key)
                quantity_obj = request.POST.get(quantity_key)
                suplyprice_obj = request.POST.get(suplyprice_key)
                tinderprice_obj = request.POST.get(tinderprice_key)
                unit_obj = request.POST.get(unit_key)
                code_obj = request.POST.get(code_key)

               
                TindetItem.objects.create(
                    tinder=tinder,
                    item=item_title,
                    quantity=quantity_obj,
                    supply_price=suplyprice_obj,
                    tinder_price=tinderprice_obj,
                    unit=unit_obj,
                    code=code_obj,
                )
            

                ii += 1
            else:
                break
        
        
        messages.success(request,'تم الحفظ بنجاح')
        return redirect('tinder:all_tinder')

    context={
        'tinder':tinder,
        'awared_by':awared_by,
        'competitor':competitor,
        
        'status_choices':status_choices,
        'insurancetype':insurancetype,
        'tinder_file':tinder_file,
        'tinder_item':tinder_item,

        
    }
    return render(request,'tinder/edit_tinder.html',context)
@login_required
def detail_tinder(request,id):
    tinder=Tinder.objects.get(id=id)
    items=TindetItem.objects.filter(tinder=tinder)
    files=TinderFiles.objects.filter(tinder=tinder)

    context={
        'tinder':tinder,
        'items':items,
        'files':files
    }
    return render(request,'tinder/detail_tinder.html',context)

@login_required
def add_tinder(request):
    
    status_choices = Tinder._meta.get_field('status').choices
    insurancetype_choices=Tinder._meta.get_field('insurance_type').choices

    company_by=Company_by.objects.all() # الشركات المعلنة
    competitor=Competitor.objects.all() # الشركات المنافسة

    category=Category.objects.all()


    context={
        'status_choices':status_choices,
        'insurancetype_choices':insurancetype_choices,
        'company_by':company_by,
        'competitor':competitor,
        'category':category,
    }
    return render(request,'tinder/add_tinder.html',context)

#



@login_required
def save_tinder(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        descriptions = request.POST.get('descriptions')
        status = request.POST.get('status')
        open_date = request.POST.get('open_date')
        close_date = request.POST.get('close_date')
        insurance_amount = request.POST.get('insurance_amount')
        insurance_type = request.POST.get('insurance_type')
        offer_value = request.POST.get('offer_value')
        company_by_id = request.POST.get('company_by')
        awared_by_id = request.POST.get('awared_by')

        tinder = Tinder.objects.create(
            title=title,
            descriptions=descriptions,
            status=status,
            open_date=open_date,
            close_date=close_date,
            insurance_amount=insurance_amount,
            insurance_type=insurance_type,
            offer_value=offer_value,
            company_by_id=company_by_id,
            awared_by_id=awared_by_id,
            created_by=request.user
        )

        # 👇 نطبع البيانات الواردة للتاكيد
        print("POST KEYS:", request.POST.keys())
        print("FILES KEYS:", request.FILES.keys())

        # ⚡ نلف على كل العناصر اللي فيها file_title
        i = 0
        while True:
            title_key = f'files_list[{i}][file_title]'
            file_key = f'files_list[{i}][file_upload]'
            if title_key in request.POST and file_key in request.FILES:
                file_title = request.POST.get(title_key)
                file_obj = request.FILES.get(file_key)

                # تحقق أنه ملف PDF
                if file_obj.name.lower().endswith('.pdf'):
                    TinderFiles.objects.create(
                        tinder=tinder,
                        title=file_title,
                        files=file_obj
                    )
                else:
                    messages.warning(request, f"❌ الملف '{file_obj.name}' ليس PDF وتم تجاهله")

                i += 1
            else:
                break  # لما يخلص الملفات نخرج من اللوب
       
        ii = 0
        while True:
            item_key = f'items_list[{ii}][item]'
            quantity_key = f'items_list[{ii}][quantity]'
            suplyprice_key = f'items_list[{ii}][supply_price]'
            tinderprice_key = f'items_list[{ii}][tinder_price]'
            unit_key = f'items_list[{ii}][unit]'
            if item_key in request.POST and suplyprice_key in request.POST and  tinderprice_key in request.POST and  unit_key in request.POST and quantity_key in request.POST:
                item_title = request.POST.get(item_key)
                quantity_obj = request.POST.get(quantity_key)
                suplyprice_obj = request.POST.get(suplyprice_key)
                tinderprice_obj = request.POST.get(tinderprice_key)
                unit_obj = request.POST.get(unit_key)

                # تحقق أنه ملف PDF
                
                TindetItem.objects.create(
                    tinder=tinder,
                    item=item_title,
                    quantity=quantity_obj,
                    supply_price=suplyprice_obj,
                    tinder_price=tinderprice_obj,
                    unit=unit_obj
                )
            

                ii += 1
            else:
                break  # 
        messages.success(request, '✅ تم حفظ المناقصة وجميع الملفات بنجاح')
        return redirect('tinder:all_tinder')

    return redirect('tinder:add_tinder')

@login_required
def edit_tinder_file(request):
    if request.method == 'POST':
        file_id=request.POST['id']
        title=request.POST.get('title')
        files=request.FILES.get('file_name')

        file_item=TinderFiles.objects.get(id=file_id)

        file_item.title=title
        file_item.files=files
        file_item.save()
        messages.success(request,'ok done')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


        
@login_required   
def delete_file(request):
    if request.method == 'POST':
        file_id=request.POST.get('id')
        file=TinderFiles.objects.get(id=file_id)
        file.delete()
        messages.success(request,'ok Done delete')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
@login_required
def edit_item(request):
    item_id=request.POST.get('id')
    item_tinder=TindetItem.objects.get(id=item_id)
    item=request.POST.get('item')
    quantity=request.POST.get('quantity')
    code=request.POST.get('code')
    supply_price=request.POST.get('supply_price')
    tinder_price=request.POST.get('tinder_price')
    unit=request.POST.get('unit')

    item_tinder.item=item
    item_tinder.quantity=quantity
    item_tinder.code=code
    item_tinder.supply_price=supply_price
    item_tinder.tinder_price=tinder_price
    item_tinder.unit=unit

    item_tinder.save()
    messages.success(request,'مبرووك تم التعديل بنجاح')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

login_required
def delete_item(request):
    item_id=request.POST.get('id')
    item=TindetItem.objects.get(id=item_id)
    item.delete()
    messages.success(request,'تم الحذف  بنجاح')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


   
    



    


