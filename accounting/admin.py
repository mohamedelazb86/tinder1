from django.contrib import admin


from .models import CashBox,CashTransaction,Category
admin.site.register(Category)
admin.site.register(CashTransaction)
admin.site.register(CashBox)
