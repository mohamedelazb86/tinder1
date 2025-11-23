from django.db import models
from settings.models import Location
from authuser.models import User
from django.utils.text import slugify
from contact.models import Supplier,Customer


class Store(models.Model):
    name=models.CharField(max_length=120)
    location=models.ForeignKey(Location,on_delete=models.SET_NULL,null=True,blank=True,related_name='store_location')
    code=models.CharField(max_length=75,null=True,blank=True)
    slug=models.SlugField(null=True,blank=True)
    notes=models.TextField(max_length=1500)
    manager=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='store_manager')

    def __str__(self):
        return self.name
    
    def save(self,*args,**kwargs):
        self.slug=slugify(self.name)
        if not self.code.startswith('in'):
            self.code='in_'+self.code
        super().save(*args,**kwargs)

class Brand(models.Model):
    name=models.CharField(max_length=120)
    notes=models.TextField(max_length=1500)
    def __str__(self):
        return self.nam
    

class Product(models.Model):
    name=models.CharField(max_length=120)
    image=models.ImageField(upload_to='image_product')
    sku=models.CharField(max_length=120)
    quantity=models.FloatField(default=0)
    brand=models.ForeignKey(Brand,related_name='product_brand',on_delete=models.SET_NULL,null=True,blank=True)
    price=models.FloatField(default=0)
    descriptions=models.TextField(max_length=1500)
    code=models.CharField(max_length=75)
    slug=models.SlugField(null=True,blank=True)
    supplier=models.ForeignKey(Supplier,related_name='product_supplier',on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self):
        return self.name
    def save(self,*args,**kwargs):
        self.slug=slugify(self.name)
        if not self.name.startswith('pro_'):
            self.code='pro_'+self.code
        super().save(*args,**kwargs)


TYPE_TRANSACTION=[
    ('IN','IN'),
    ('OUT','OUT'),

]

class InventoryTransaction(models.Model):
    store=models.ForeignKey(Store,related_name='transaction_store',on_delete=models.CASCADE)
    product=models.ForeignKey(Product,related_name='transaction_product',on_delete=models.SET_NULL,null=True,blank=True)
    supplier=models.ForeignKey(Supplier,related_name='transactions_supplier',on_delete=models.SET_NULL,null=True,blank=True)
    customer=models.ForeignKey(Customer,related_name='transactions_customer',on_delete=models.SET_NULL,null=True,blank=True)
    quantity=models.FloatField(default=0)
    type=models.CharField(max_length=25,choices=TYPE_TRANSACTION)
    
    def __str__(self):
        return str(self.store)

    
class PurchaseOrder(models.Model):
    store=models.ForeignKey(Store,related_name='transaction_order',on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE,related_name='PurchaseOrder_supplier')
    
    invoice_number = models.CharField(max_length=100, unique=True)
    date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    

    def __str__(self):
     return f"PO-{self.invoice_number}"

class PurchaseItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField()
    price = models.FloatField()


    def total(self):
        return self.quantity * self.price
    
class SalesOrder(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=200)
    invoice_number = models.CharField(max_length=100, unique=True)
    date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return f"SO-{self.invoice_number}"




class SalesItem(models.Model):
    sales_order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField()
    price = models.FloatField()


    def total(self):
        return self.quantity * self.price


    


