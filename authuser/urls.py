from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name='authuser'

urlpatterns = [

    path('login',views.LoginView.as_view(),name='login'),
    path('logout',views.LogooutView.as_view(),name='logout'),
    path('all_user',login_required(views.all_user),name='all_user'),
    path('active_user',login_required(views.active_user),name='active_user'),
    path('deactive_user',login_required(views.deactive_user),name='deactive_user'),

    path('add_user',views.add_user,name='add_user'),
    path('save_user',views.save_user,name='save_user'),
    path('edit_user/<int:id>',views.edit_user,name='edit_user'),

    path('edit_profile',views.edit_profile,name='edit_profile'),

]
