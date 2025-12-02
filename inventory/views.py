from django.shortcuts import render,redirect
from .models import Product,Brand,MainItem,Store
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from settings.models import Location
from authuser.models import User



@login_required
def products(request):
    products=Product.objects.all().order_by('-id')
    context={
        'products':products
    }
    return render(request,'inventory/products.html',context)


@login_required
def add_product(request):
    brands=Brand.objects.all()
    mainitems=MainItem.objects.all()
    context={
        'brands':brands,
        'mainitems':mainitems
    }
    return render(request,'inventory/add_product.html',context)


@login_required
def save_product(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        brand=request.POST.get('brand')
        mainitem=request.POST.get('mainitem')
        supplier=request.POST.get('supplier')
        descriptions=request.POST.get('descriptions')
        image=request.POST.get('image')
        sku=request.POST.get('sku')

        Product.objects.create(
            name=name,
            brand_id=brand,
            mainitem_id=mainitem,
            supplier_id=supplier,
            descriptions=descriptions,
            image=image,
            sku=sku

        )
        messages.success(request,'تم الحفظ')
        return redirect('inventory:products')
    
@login_required   
def delete_product(request):
    if request.method =='POST':
        product_id=request.POST.get('id')
        product=Product.objects.get(id=product_id)
        product.delete()
        messages.success(request,'تم الحذف بنجاح')
        return redirect('inventory:products')


@login_required
def update_product(request,id):

   
    product=Product.objects.get(id=id)
    brands=Brand.objects.all()
    mainitems=MainItem.objects.all()
    
    if request.method =='POST':
        

        name=request.POST.get('name')
        sku=request.POST.get('sku')
        brand=request.POST.get('brand')
        mainitem=request.POST.get('mainitem')
        supplier=request.POST.get('supplier')
        image=request.FILES.get('image')
        descriptions=request.POST.get('descriptions')

        product.name=name
        product.sku=sku,
        product.brand_id=brand
        product.mainitem_id=mainitem
        product.supplier_id=supplier
        product.image=image
        product.descriptions=descriptions

        product.save()
        messages.success(request,'تم التعديل بنجاح')
        return redirect('inventory:products')
    context={
        'product':product,
        'brands':brands,
        'mainitems':mainitems
    }
    return render(request,'inventory/update_product.html',context)

@login_required
def product_detail(request,id):
    product=Product.objects.get(id=id)
    context={
        'product':product
    }
    return render(request,'inventory/product_detail.html',context)



    
# functions for Store App

@login_required
def all_store(request):
    stores=Store.objects.all()
    context={
        'stores':stores
    }
    return render(request,'inventory/stores.html',context)
@login_required
def add_store(request):
    locations=Location.objects.all()
    users=User.objects.all()

    context={
        'locations':locations,
        'users':users
        
    }
    return render(request,'inventory/add_store.html',context)

@login_required
def save_store(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        location= request.POST.get('location')
        manager=request.POST.get('manager')
        notes=request.POST.get('notes')

        Store.objects.create(
            name=name,
            location_id=location,
            manager_id=manager,
            notes=notes
        )
        messages.success(request,'تم الحفظ بنجاح')
        return redirect('inventory:all_store')
    
@login_required
def delete_store(request):
    if request.method =='POST':
        store_id=request.POST.get('id')
        store=Store.objects.get(id=store_id)
        store.delete()
        messages.success(request,'تم الحذف بنجاح')
        return redirect('inventory:all_store')
    
    
@login_required
def edit_store(request,id):

    store=Store.objects.get(id=id)
    locations=Location.objects.all()
    users=User.objects.all()

    if request.method == 'POST':
        name=request.POST.get('name')
        location=request.POST.get('location')
        manager=request.POST.get('manager')
        notes=request.POST.get('notes')

        store.name=name
        store.location_id=location
        store.manager_id=manager
        store.notes=notes

        store.save()
        messages.success(request,'تم التعديل بنجاح')
        return redirect('inventory:all_store')
        

    context={
        'store':store,
        'locations':locations,
        'users':users
    }
    return render(request,'inventory/edit_store.html',context)
@login_required
def store_detail(request,id):
    store=Store.objects.get(id=id)
    context={
        'store':store
    }
    return render(request,'inventory/detail_store.html',context)
    


    