from django.urls import path
from . import views

app_name='accounting'

urlpatterns = [
    path('',views.all_cashbox,name='all_cashbox'),
    path('add_cashbox',views.add_cashbox,name='add_cashbox'),
    path('edit_cashbox/<int:id>',views.edit_cashbox,name='edit_cashbox'),

    path('active',views.active_cashbox,name='active'),
    path('deactive',views.deactive,name='deactive'),

    path('all_transaction',views.all_transaction,name='all_transaction'),
]
