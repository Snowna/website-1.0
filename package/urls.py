from django.urls import path
from . import views

app_name = 'package'

urlpatterns = [
    # /package/---main page for all the users
    path('', views.index, name='index'),
    # /package/index/
    path('<int:package_id>/', views.detail, name='detail'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout_user'),
    path('login_user/', views.login_user, name='login_user'),
    path('create_package/', views.create_package, name='create_package'),
]