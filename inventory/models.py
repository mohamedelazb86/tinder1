from django.db import models
from settings.models import Location
from authuser.models import User
from django.utils.text import slugify
from contact.models import Supplier,Customer
import re
from django.db import models
from django.core.exceptions import ValidationError


class Store(models.Model):
    name=models.CharField(max_length=120)
    location=models.ForeignKey(Location,on_delete=models.SET_NULL,null=True,blank=True,related_name='store_location')
    code=models.CharField(max_length=75,null=True,blank=True)
    code_no=models.IntegerField(null=True,blank=True)
    slug=models.SlugField(null=True,blank=True)
    notes=models.TextField(max_length=1500)
    manager=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='store_manager')

    def __str__(self):
        return self.name
         
       
    def save(self, *args, **kwargs):

        if not self.code: 
            last_store=Store.objects.filter().order_by('-id').first()
            if last_store and last_store.code and last_store.code_no :
                next_number= int(last_store.code_no) + 1
            else:
                next_number = 1
            self.code=f'ST_{next_number}'
            self.code_no=next_number
  
        super().save(*args, **kwargs)
        
    

      
        

class Brand(models.Model):
    name=models.CharField(max_length=120)
    code=models.CharField(max_length=120,null=True,blank=True, unique=True)
    code_no=models.IntegerField(null=True, blank=True)
    notes=models.TextField(max_length=1500)
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):

        if not self.code:  

           
            last_brand = Brand.objects.all().order_by("-id").first()
         
            if last_brand and last_brand.code and last_brand.code_no:
               
                next_number = int(last_brand.code_no) + 1
            else:
                next_number = 1

            self.code = f"BR-{next_number}"
            self.code_no = next_number

       
        super().save(*args, **kwargs)

class MainItem(models.Model):
    name=models.CharField(max_length=120)
    code=models.CharField(max_length=120,null=True,blank=True,unique=True)
    code_no=models.IntegerField(null=True,blank=True)
    notes=models.TextField(max_length=1500)
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):

        if not self.code:  
            last_mainitem=MainItem.objects.filter().order_by('-id').first()
            if last_mainitem and last_mainitem.code and last_mainitem.code_no:
                next_number=int(last_mainitem.code_no) + 1
            else:
                next_number=1
            self.code_no=next_number
            self.code=F'MI_{next_number}'
            
        super().save(*args,**kwargs)

        


class Product(models.Model):
    name=models.CharField(max_length=120)
    image=models.ImageField(upload_to='image_product',null=True, blank=True)
    sku=models.CharField(max_length=120)
    # quantity=models.FloatField(default=0)
    brand=models.ForeignKey(Brand,related_name='product_brand',on_delete=models.SET_NULL,null=True,blank=True)
    descriptions=models.TextField(max_length=1500)
    code=models.CharField(max_length=75,null=True,blank=True)
    code_no=models.IntegerField(null=True, blank=True)
    slug=models.SlugField(null=True,blank=True)
    supplier=models.ForeignKey(Supplier,related_name='product_supplier',on_delete=models.SET_NULL,null=True,blank=True)
    mainitem=models.ForeignKey(MainItem,related_name='product_mainitem',on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)

        
        if self.pk:      # اذا كان المنتج موجود بالفعل 
            try:
                old_instance = Product.objects.get(pk=self.pk)    #  هات المنتج القديم   
                if old_instance.brand != self.brand or old_instance.mainitem  != self.mainitem:    #  هل البراند والبند الرئيسي الجديد لا يساوي القديم معني كده حصل تعديل في ايهم 
                   self.code = f"{self.mainitem.code}-{self.brand.code}-{old_instance.code_no}"   # سجل الكود مره تانية بالبيانات الجديدة

            except Product.DoesNotExist:
                pass
        

        elif not self.code:
            last_product = Product.objects.filter(
                mainitem=self.mainitem,
                brand=self.brand
            ).order_by('-id').first()

            if last_product and last_product.code and last_product.code_no:
                

                next_number = int(last_product.code_no) + 1 


            else:
                next_number = 1

            self.code = f"{self.mainitem.code}-{self.brand.code}-{next_number}"
            self.code_no=next_number

        
        

        super().save(*args, **kwargs)

    


TYPE_TRANSACTION=[
    ('IN','IN'),
    ('OUT','OUT'),

]

class Transaction(models.Model):
    store=models.ForeignKey(Store,related_name='transaction_store',on_delete=models.CASCADE)
    product=models.ForeignKey(Product,related_name='transaction_product',on_delete=models.SET_NULL,null=True,blank=True)
    supplier=models.ForeignKey(Supplier,related_name='transactions_supplier',on_delete=models.SET_NULL,null=True,blank=True)
    customer=models.ForeignKey(Customer,related_name='transactions_customer',on_delete=models.SET_NULL,null=True,blank=True)
    quantity=models.FloatField(default=0)
    price=models.FloatField(default=0)
    type=models.CharField(max_length=25,choices=TYPE_TRANSACTION)
    date=models.DateField()
    transation_no=models.IntegerField()
    
    def __str__(self):
        return str(self.store)
    


TYPE_ORDER=[
    ('IN','IN'),
    ('OUT','OUT'),

] 
CANCEL =[
    ('OPEN','OPEN'),
    ('APPENDING','APPENDING'),
    ('FINISH','FINISH'),
    ('CANCEL','CANCEL'),
    ]
class Order(models.Model):
    store=models.ForeignKey(Store,related_name='store_order',on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE,related_name='Order_supplier')
    customer=models.ForeignKey(Customer,related_name='order_customer',on_delete=models.SET_NULL,null=True,blank=True)
    type=models.CharField(max_length=75,choices=TYPE_ORDER)
    order_number = models.CharField(max_length=100, unique=True)
    date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    stauts=models.CharField(max_length=100,choices=CANCEL)
    

    def __str__(self):
     return f"PO-{self.order_number}"

class PurchaseItem(models.Model):    #فاتورة الشراء
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items_purchase")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField()
    price = models.FloatField()


    def total(self):
        return self.quantity * self.price
    




class DispenseItem(models.Model): # فاتورة البيع
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items_dispense")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField()
    price = models.FloatField()


    def total(self):
        return self.quantity * self.price


    


