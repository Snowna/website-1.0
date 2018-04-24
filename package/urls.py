from django.urls import path
from . import views

app_name = 'package'

urlpatterns = [
    # /package/---main page for all the users
    path('', views.index_v, name='index_v'),
    # /package/index/
    path('index/', views.index, name='index'),
    path('<int:package_id>/', views.detail, name='detail'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout_user'),
    path('login_user/', views.login_user, name='login_user'),
    path('create_package/', views.create_package, name='create_package'),
    path('<int:package_id>/delete_package/', views.delete_package, name='delete_package'),
    path('index/profile/', views.profile, name='profile'),
]
