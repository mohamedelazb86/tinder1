from django.urls import path
from . import views

app_name='myproject'

urlpatterns = [
    path('<int:id>',views.myproject,name='myproject'),
    # path('create_project/<int:id>',views.create_project,name='create_project'),
    path('edit_item_',views.edit_item,name='edit_item'),
    path('project_detail/<int:id>',views.project_detail,name='project_detail'),
]
