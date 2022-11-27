from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home1'),
    path('home/',views.home,name='home2')
]