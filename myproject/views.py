from django.shortcuts import render,redirect
from .models import Project,ProjectItem
from tinder.models import Tinder,TindetItem
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect



@login_required
def myproject(request,id):
    STATUS_PROJECT = Project._meta.get_field("status").choices
    tinder=Tinder.objects.get(id=id)
    items=TindetItem.objects.filter(tinder=tinder)
    project1=Project.objects.filter(tinder=tinder).first()

    if request.method == 'POST':
        tinder=Tinder.objects.get(id=id)
        title=request.POST.get('title')
        created_at=request.POST.get('created_at')
        created_by=request.user
        desciptions=request.POST.get('desciptions')
        status=request.POST.get('status')
        code=request.POST.get('code')
        begin_project=request.POST.get('begin_project')
        duration=request.POST.get('duration')

        project=Project.objects.create(
            tinder=tinder,
            title=title,
            created_at=created_at,
            created_by=created_by,
            desciptions=desciptions,
            status=status,
            code=code,
            begin_project=begin_project,
            duration=duration

       )
  

        for item in items:
            ProjectItem.objects.create(
                project=project,
                statment=item.statment,
                item=item.item,
                quantity=item.quantity,
                price=item.supply_price,
                unit=item.unit,
                total=item.total
            )
           

      

        project.save()
        messages.success(request,'تم الحفظ')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



    
    context={
        'STATUS_PROJECT':STATUS_PROJECT,
        'tinder':tinder,
        'items':items,
        'project1':project1,
    }
    return render(request,'myproject/project.html',context)

# @login_required
# def create_project(request,id):
    
#     if request.method == 'POST ':
#         tinder=Tinder.objects.get(id=id)
#         title=request.POST.get('title')
#         created_at=request.POST.get('created_at')
#         created_by=request.user
#         desciptions=request.POST.get('desciptions')
#         status=request.POST.get('status')
#         code=request.POST.get('code')
#         begin_project=request.POST.get('begin_project')
#         duration=request.POST.get('duration')

#         project=Project.objects.create(
#             tinder_id=tinder,
#             title=title,
#             created_at=created_at,
#             created_by=created_by,
#             desciptions=desciptions,
#             status_id=status,
#             code=code,
#             begin_project=begin_project,
#             duration=duration

#         )

        
#         statments=request.POST.getlist('statment[]')
#         items=request.POST.getlist('item[]')
#         quantitys=request.POST.getlist('quantity[]')
#         prices=request.POST.getlist('price[]')
#         units=request.POST.getlist('unit[]')
#         totals=request.POST.getlist('total[]')

#         if statments and items and quantitys and prices and units and totals :
#             for s,i,q,p,u,t in zip(statments,items,quantitys,prices,units,totals):
#                 ProjectItem.objects.create(
#                     project=project,
#                     statment=s,
#                     quantity=q,
#                     price=p,
#                     unit=u,
#                     total=t
#                 )
#         messages.success(request,'تم الحفظ بنجاح')
#         return redirect('tinder:all_tinder')
#     return render(request,'myproject/project.html')

@login_required
def edit_item(request):
    item_id=request.POST.get('id')
    item_tinder=TindetItem.objects.get(id=item_id)
    item=request.POST.get('item')
    quantity=request.POST.get('quantity')
    code=request.POST.get('code')
    
    price=request.POST.get('price')
    unit=request.POST.get('unit')
    statment=request.POST.get('statment')

    item_tinder.item=item
    item_tinder.quantity=quantity
    item_tinder.code=code
    item_tinder.supply_price=price
    
    item_tinder.unit=unit
    item_tinder.statement=statment

    item_tinder.save()
  
    messages.success(request,'مبرووك تم التعديل بنجاح')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
def project_detail(request,id):
    return render(request,'myproject/project_detail.html',{})

        
        
        
