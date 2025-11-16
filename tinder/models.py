from django.db import models
from utils.generate_code import generate_code
from authuser.models import User
from django.core.exceptions import ValidationError
from contact.models import Competitor,Company_by
from django.utils import timezone
import os


STATUS_TINDER=[
    ('DRAFT','DRAFT'),
    ('OPEN','OPEN'),
    ('CLOSED','CLOSED'),
    ('CANCEL','CANCEL'),
    ('AWARED','AWARED'),

]
INSURANCE_TYPE=[
    ('CASH','CASH'),
    ('CHEQUE','CHEQUE'),
    ('BANK_GUARANTEE','BANK_GUARANTEE'),
]

    # Data Base for Tinder
class Tinder(models.Model):
    code=models.CharField(max_length=75,default=generate_code)
    title=models.CharField(max_length=120)
    descriptions=models.TextField(max_length=1500)
    status=models.CharField(max_length=75,choices=STATUS_TINDER)
    
    created_at=models.DateTimeField(default=timezone.now())
    open_date=models.DateTimeField()
    close_date=models.DateTimeField()
    insurance_amount=models.FloatField()
    insurance_type=models.CharField(max_length=120,choices=INSURANCE_TYPE)
    awared_by=models.ForeignKey(Competitor,related_name='tinder_supplier',on_delete=models.SET_NULL,null=True,blank=True) # الشركات المنافسة
    offer_value=models.FloatField()
    created_by=models.ForeignKey(User,related_name='tinder_user',on_delete=models.SET_NULL,null=True,blank=True)
    company_by=models.ForeignKey(Company_by,related_name='tinder_supplier',on_delete=models.SET_NULL,null=True,blank=True) # الشركة المعنلة عن المناقصة


    class Meta:
        indexes =[
            models.Index(fields=['code']),
            models.Index(fields=['status'])
            
        ]

    def __str__(self):
        return str(self.title)
    
    def save(self,*args,**kwargs):
        if not self.code.startswith('tr_'):
             self.code='tr_'+self.code
        if self.close_date <= self.open_date:
             raise ValidationError('sorry this date not valid')
        
         # ✅ 3) إذا كانت المناقصة مغلقة أو مرساة يجب أن يكون لها فائز
        if self.status in ['closed', 'awared'] and not self.awared_by:
            raise ValidationError('❌ لا يمكن حفظ مناقصة مغلقة أو مرساة بدون تحديد الشركة الفائزة.')
        
        super().save(*args,**kwargs)


def tender_file_upload_path(instance, filename):
    # نحاول نستخدم كود المناقصة لو موجود
    if instance.tinder and instance.tinder.code:
        return f'files_tinder/Documents/{instance.tinder.code}/{filename}'
    return f'files_tinder/Documents/unknown/{filename}'


class TinderFiles(models.Model):
    tinder = models.ForeignKey(Tinder, related_name='filestinder', on_delete=models.CASCADE)
    files = models.FileField(upload_to=tender_file_upload_path)
    title = models.CharField(max_length=120)



    def save(self,*args,**kwargs):
        if self.pk:
            try:
                old_instance = TinderFiles.objects.get(pk=self.pk)
                if old_instance.files and self.files and old_instance.files != self.files:
                    if os.path.isfile(old_instance.files.path):
                        os.remove(old_instance.files.path)  # Delete old file

            except TinderFiles.DoesNotExist:
                pass

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    


class TindetItem(models.Model):
     tinder=models.ForeignKey(Tinder,related_name='item_tinder',on_delete=models.CASCADE)
     item=models.CharField(max_length=120)
     quantity=models.FloatField()
     code=models.CharField(max_length=25,null=True,blank=True)
     supply_price=models.FloatField(null=True,blank=True)
     tinder_price=models.FloatField(null=True,blank=True)
     unit=models.CharField(max_length=25,default='pice')

     def __str__(self):
          return self.item
     
     def save(self,*args,**kwargs):
          if not self.code.startswith('it_'):
               self.code='it_'+self.code
          super().save(*args,**kwargs)
