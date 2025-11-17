from django.db import models
from authuser.models import User


CASHBOX_TYPE=[
    ('CASH','نقدي'),
    ('CHEQUE','شيكات'),
]
# انشاء الخزينة بصفة عامة سواء نقدى أو شيكات
class CashBox(models.Model):        # الخزينة
    name=models.CharField(max_length=120)
    type=models.CharField(max_length=75,choices=CASHBOX_TYPE)
    is_main=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    treasurer=models.ForeignKey(User,related_name='cash_treasurer',on_delete=models.SET_NULL,null=True,blank=True)  # أمين الخزينة
    details=models.TextField(max_length=1500)

    created_at=models.DateTimeField(auto_now_add=True)
    edit_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    
# انش اء حركة الخزينة  من وراد ومنصرف للخزينة دى
class CashTransaction(models.Model):        # حركة الخزينة
    cashbox=models.ForeignKey(CashBox,related_name='transaction_cashbox',on_delete=models.CASCADE)        # أسم الخزينة
    date_transaction=models.DateTimeField()           # تاريخ الحركة
    no=models.IntegerField()                          # رقم الايصال
    category=models.ForeignKey('Category',related_name='transaction_category',on_delete=models.SET_NULL,null=True,blank=True)
    inbox=models.FloatField(null=True,blank=True)       # الوارد
    absentminded=models.FloatField(null=True,blank=True)  # المنصرف

    def __str__(self):
        return str(self.category)
    

CATEGORY_TYPE=[
    ('IN','IN'),
    ('OUT','OUT'),
] 
# انشاء التصنيف لحركة الخزين  سواء كان م.إدارية  أو مصاريف تشغيل فى حالة الصرف  لو فى حالة التوريد فى مسمسات أخرى
class Category(models.Model):            # التصنيف
    name=models.CharField(max_length=120)
    type=models.CharField(max_length=120,choices=CATEGORY_TYPE)

    def __str__(self):
        return self.name
