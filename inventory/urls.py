from django.urls import path
from . import views

app_name='inventory'

urlpatterns = [
    path('products',views.products,name='products'),
    path('add_product',views.add_product,name='add_product'),
    path('save_product',views.save_product,name='save_product'),
    path('update_product/<int:id>',views.update_product,name='update_product'),
    path('delete_product',views.delete_product,name='delete_product'),
    path('product_detail/<int:id>',views.product_detail,name='product_detail'),

    # store
    path('all_store',views.all_store,name='all_store'),
    path('add_store',views.add_store,name='add_store'),
    path('save_store',views.save_store,name='save_store'),
    path('delete_store',views.delete_store,name='delete_store'),
    path('edit_store/<int:id>',views.edit_store,name='edit_store'),
    path('detail_store/<int:id>',views.store_detail,name='detail_store'),

    #brand
    path('brands',views.brands,name='brands'),
    path('add_brand',views.add_brand,name='add_brand'),
    path('delete_brand',views.delete_brand,name='delete_brand'),
    path('edit_brand/<int:id>',views.edit_brand,name='edit_brand'),

    #mainitem
    path('mainitem',views.mainitem,name='mainitem'),
    path('add_mainitem',views.add_mainitem,name='add_mainitem'),
    path('delete_mainitem',views.delete_mainitem,name='delete_mainitem'),
    path('edit_mainitem/<int:id>',views.edit_mainitem,name='edit_mainitem'),

    # transaction
    path('transaction',views.transaction,name='transactions'),
    path('supply_permit',views.supply_permit,name='supply_permit'),
    path('purchase',views.add_purchase,name='add_purchase'),
    
    path('trans_detail/<int:id>',views.trans_detail,name='trans_detail'),
    path('save_transdetail',views.save_transdetail,name='save_transdetail'),
    
    


]
