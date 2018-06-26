from django.urls import path
from . import views

app_name = 'basicapp'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='user_login')
]
