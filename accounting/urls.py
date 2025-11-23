from django.urls import path
from . import view1
from . import view

app_name='accounting'

urlpatterns = [
    path('',view.all_cashbox,name='all_cashbox'),
    path('add_cashbox',view.add_cashbox,name='add_cashbox'),
    path('edit_cashbox/<int:id>',view1.edit_cashbox,name='edit_cashbox'),

    path('active',view.active_cashbox,name='active'),
    path('deactive',view.deactive,name='deactive'),

    path('mytrannsaction/<int:id>',view.transaction,name='transaction'),
    path('add_inbox',view.add_inbox,name='add_inbox'),
    path('add_absentminded',view.add_absentminded,name='add_absentminded'),

   
]
