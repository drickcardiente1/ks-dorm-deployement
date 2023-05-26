from django.urls import path
from . import views

urlpatterns = [
    path('login_user', views.login_user, name="login"),
    path('login_modal', views.login_modal, name="login_modal"),
    path('logout_user/', views.logout_user, name='logout'),
]