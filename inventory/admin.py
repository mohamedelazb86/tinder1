from django.contrib import admin

from .models import Store,Brand,Product,PurchaseItem,Order,DispenseItem,Transaction,MainItem

admin.site.register(Store)
admin.site.register(Product)
admin.site.register(Brand)
admin.site.register(PurchaseItem)
admin.site.register(Order)
admin.site.register(DispenseItem)
admin.site.register(MainItem)

admin.site.register(Transaction)
