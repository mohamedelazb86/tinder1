from django.db import models
from django.core.exceptions import ValidationError


class Category(models.Model):
    name=models.CharField(max_length=120)

    def __str__(self):
        return self.name
    
def validate_number(number):
    if len(number) != 11 or not number.isdigit():
        raise ValidationError('sorry this number not valid')
    
STATUS_SUPPLIER=[
    ('ACTIVE','ACTIVE'),
    ('INACTIVE','INACTIVE'),
]

class Supplier(models.Model):
    code=models.CharField(max_length=75,unique=True)
    name=models.CharField(max_length=120)
    email=models.CharField(max_length=100,null=True,blank=True)
    phone=models.CharField(max_length=25,validators=[validate_number])
    category=models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True,related_name='supplier_category')
    balance=models.FloatField(default=0)
    status=models.CharField(max_length=120,choices=STATUS_SUPPLIER)
    notes=models.CharField(max_length=1500)

    class Meta:
        indexes=[
            models.Index(fields=['code']),
            models.Index(fields=['name','category'])

        ]
    def __str__(self):
        return self.name
    
    def save(self,*args,**kwargs):
        if not self.code.startswith('sup_'):
            self.code='sup_'+self.code
        super().save(*args,**kwargs)

class Competitor(models.Model): # الشركات المنافسة
    code=models.CharField(max_length=75,unique=True)
    name=models.CharField(max_length=120)
    email=models.CharField(max_length=100,null=True,blank=True)
    phone=models.CharField(max_length=25,validators=[validate_number])
    category=models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True,related_name='Competitor_category')
    notes=models.CharField(max_length=1500)

    class Meta:
        indexes=[
            models.Index(fields=['code']),
            models.Index(fields=['name','category'])

        ]
    def __str__(self):
        return self.name
    
    def save(self,*args,**kwargs):
        if not self.code.startswith('com_'):
            self.code='com_'+self.code
        super().save(*args,**kwargs)

class Company_by(models.Model):  # الشركات المعنلة
    code=models.CharField(max_length=75,unique=True)
    name=models.CharField(max_length=120)
    email=models.CharField(max_length=100,null=True,blank=True)
    phone=models.CharField(max_length=25,validators=[validate_number])
    tax_file=models.FileField(upload_to='tax_file')
   
    notes=models.CharField(max_length=1500)

    class Meta:
        indexes=[
            models.Index(fields=['code']),
            models.Index(fields=['name'])

        ]
    def __str__(self):
        return self.name
    
STATUS_CUSTOMER=[
    ('ACTIVE','ACTIVE'),
    ('INACTIVE','INACTIVE'),
]

class Customer(models.Model):
    code=models.CharField(max_length=75,unique=True)
    name=models.CharField(max_length=120)
    email=models.CharField(max_length=100,null=True,blank=True)
    phone=models.CharField(max_length=25,validators=[validate_number])
    # category=models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True,related_name='supplier_category')
    balance=models.FloatField(default=0)
    status=models.CharField(max_length=120,choices=STATUS_CUSTOMER)
    notes=models.CharField(max_length=1500)

    class Meta:
        indexes=[
            models.Index(fields=['code']),
            models.Index(fields=['name'])

        ]
    def __str__(self):
        return self.name
    

