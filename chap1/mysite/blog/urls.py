from django.urls import path
from . import views

#! app_name variable is used to organize URLS by application and use the name to refer to them
#? ex. blog:post_list
app_name = 'blog'


urlpatterns = [
    #! name is used for each specific url in project-wide
    path('', views.post_list, name='post_list'),

    #! use brackets to capture URL values
    path('<int:pk>/', views.post_detail, name='post_detail'),
]