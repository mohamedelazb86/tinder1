from django.contrib import admin

from .models import Store,Brand,Product,PurchaseItem,PurchaseOrder,SalesItem,SalesOrder,InventoryTransaction

admin.site.register(Store)
admin.site.register(Product)
admin.site.register(Brand)
admin.site.register(PurchaseItem)
admin.site.register(PurchaseOrder)
admin.site.register(SalesItem)
admin.site.register(SalesOrder)
admin.site.register(InventoryTransaction)
