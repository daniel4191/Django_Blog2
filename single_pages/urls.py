from django.urls import path
from . import views

app_name = 'sigle_pages'

urlpatterns = [
    path('', views.landing),
    path('about_me/', views.about_me)
]