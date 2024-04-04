from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('register/', views.register_user, name='register_user'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('guitar_info/', views.guitar_info, name='guitar_info'),

    # other URL patterns
]
