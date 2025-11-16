from django.db import models
from utils.generate_code import generate_code

class Sector(models.Model):
    code=models.CharField(max_length=75,default=generate_code)
    name=models.CharField(max_length=120)
    notes=models.TextField(max_length=1500)

    def save(self,*args,**kwargs):
        self.code='sector'+"_"+self.code
        super().save(*args,**kwargs)

    def __str__(self):
        return self.name
    
