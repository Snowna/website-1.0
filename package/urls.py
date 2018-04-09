from django.urls import path
from . import views

app_name = 'package'

urlpatterns = [
    # /package/---main page for all the users
    path('', views.index, name='index'),
    # /package/index/
    path('<int:package_id>/', views.detail, name='detail'),
    path('login/', views.login_user, name='login'),
    path('register/', views.UserFormView.as_view(), name='register'),
    path('login_user/', views.login_user, name='login_user'),
]