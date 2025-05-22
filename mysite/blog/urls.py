from django.urls import path
from . import views

#! app_name variable is used to organize URLS by application and use the name to refer to them
#? ex. blog:post_list
app_name = 'blog'


urlpatterns = [
    #! name is used for each specific url in project-wide
    #? function view to class-based view
    path('', views.PostListView.as_view(), name='post_list'),
    # path('', views.post_list, name='post_list'),

    #! use brackets to capture URL values
    # path('<int:pk>/', views.post_detail, name='post_detail'),
    #? SCO friendly URL
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),

    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
]