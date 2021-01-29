from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url,include
from django.urls import path
from . import views


urlpatterns=[
    path('',views.home,name = 'home'),
    path('signup/',views.signup , name='signup'),
    path('create_neighbourhood/',views.create_neighbourhood , name='create_neighbourhood'),
    path('system_admin/',views.system_admin,name='system_admin'),
    path('del_neighbourhood/<neighbourhood_name>/', views.del_neighbourhood, name='del_neighbourhood'),
    path('edit_neighbourhood/<neighbourhood_name>/', views.edit_neighbourhood, name='edit_neighbourhood'),
    path('del_user/<username>/', views.del_user, name='del_user'),
    path('profile/<username>/', views.profile, name='profile'),
    path('post/<id>',views.post, name='post'),
    path('neighbourhood_admin/',views.neighbourhood_admin,name='neighbourhood_admin'),
    path('create_neighbourhood_info/',views.create_neighbourhood_info , name='create_neighbourhood_info'),
    path('search',views.search_department,name = 'search_department'),
]