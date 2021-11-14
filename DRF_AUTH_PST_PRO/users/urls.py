from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register', views.registerView.as_view(), name='register'),
    path('login', views.loginView.as_view(), name='login'),
    path('user', views.userView.as_view(), name='user'),
    path('logout', views.logoutView.as_view(), name='logout')
]
