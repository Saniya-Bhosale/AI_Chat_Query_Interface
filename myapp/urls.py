
from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_interface, name='chat_interface'),
    path('get_user_data/', views.get_user_data, name='get_user_data'),
]
