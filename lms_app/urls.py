from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('test', views.test),
    # path('Lisa', views.Lisa),
    # path('grade', views.grade)
    # path('profile', views.profile), 
]