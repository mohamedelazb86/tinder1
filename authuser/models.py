from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from settings.models import Sector


def validate_number(num):
    if len(num) != 11 or not num.isdigit():
        raise ValidationError('Sorry this Number Not Valid ,Pls Try Agin')


class User(AbstractUser):
    full_name=models.CharField(max_length=120)
    phone=models.CharField(max_length=25,validators=[validate_number])
    job=models.CharField(max_length=120)
    email=models.CharField(max_length=75,null=True,blank=True)
    image=models.ImageField(upload_to='photo_user',null=True,blank=True,default='photo_user/0.jpg')
    notes=models.TextField(max_length=1500,null=True,blank=True)
    sector=models.ForeignKey(Sector,related_name='user_sector',on_delete=models.SET_NULL,null=True,blank=True)


    first_name=None
    last_name=None

    def save(self,*args,**kwargs):
        if self.username:
            self.username=self.username.lower()
        super().save(*args,**kwargs)

    def __str__(self):
        return self.full_name


