from django.db import models

# Create your models here.
from django.db import models
from tinder.models import Tinder,TindetItem
from authuser.models import User
from django.utils import timezone

STATUS_PROJECT=[
    ('NEW','جديد'),
    ('INPROGRESS','مازال مستمر'),
    ('COMPLETED','تم الانتهاء'),
]

class Project(models.Model):
    tinder=models.OneToOneField(Tinder,related_name='tender_project',on_delete=models.CASCADE)
    title=models.CharField(max_length=120)
    created_at=models.DateField(default=timezone.now(),null=True,blank=True)
    created_by=models.ForeignKey(User,related_name='project_user',on_delete=models.SET_NULL,null=True,blank=True)
    desciptions=models.TextField(max_length=1500)
    status=models.CharField(max_length=75,default='NEW',choices=STATUS_PROJECT)
    code=models.CharField(max_length=120,null=True,blank=True)
    begin_project=models.DateTimeField(null=True,blank=True)       # بداية المشروع
    duration=models.IntegerField()   # مدة المشروع

    def __str__(self):
        return self.title
    def save(self,*args,**kwargs):
        if self.code:
            if not self.code.startswith('PRJ_'):
                self.code='PRJ_'+self.code
            super().save(*args,**kwargs)

class ProjectItem(models.Model):
    project=models.ForeignKey(Project,related_name='project',on_delete=models.CASCADE)
    statment=models.TextField(max_length=120)
    item=models.CharField(max_length=120)
    quantity=models.FloatField()
    price=models.FloatField()
    unit=models.CharField(max_length=75, default='pice')
    total=models.FloatField(default=0)

    def __str__(self):
        return str(self.project)
    def save(self,*args,**kwargs):
        if self.quantity and self.price:
            self.total=self.quantity * self.price
    
class ProjectAction(models.Model):
    project=models.ForeignKey(Project,related_name='action_project',on_delete=models.CASCADE)
    details=models.TextField(max_length=1500)
    created_by=models.ForeignKey(User,related_name='actiom_created',on_delete=models.CASCADE)
    datetime=models.DateTimeField(default=timezone.now())

    def __str__(self):
        return str(self.created_by)






