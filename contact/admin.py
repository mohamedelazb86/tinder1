from django.contrib import admin

from .models import Competitor,Company_by,Category,Customer,Supplier

admin.site.register(Company_by)
admin.site.register(Competitor)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Supplier)


