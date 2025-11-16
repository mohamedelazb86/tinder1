from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name='tinder'

urlpatterns = [

    path('all_tinder',login_required(views.all_tinder),name='all_tinder'),
    path('delete_tinder',login_required(views.delete_tinder),name='delete_tinder'),
    path('edit_tinder/<int:id>',login_required(views.edit_tinder),name='edit_tinder'),
    path('detail_tinder/<int:id>',login_required(views.detail_tinder),name='detail_tinder'),
    path('add_tinder',login_required(views.add_tinder),name='add_tinder'),
    path('save_tinder',login_required(views.save_tinder),name='save_tinder'),

    path('edit_tinder_file',login_required(views.edit_tinder_file),name='edit_tinder_file'),
    path('delete_file/<int:id>',login_required(views.delete_file),name='delete_file'),

    path('edit_item',login_required(views.edit_item),name='edit_item'),
    path('delete_item',login_required(views.delete_item),name='delete_item'),
]

