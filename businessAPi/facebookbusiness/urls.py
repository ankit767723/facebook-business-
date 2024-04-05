from django.urls import path
from. import views

urlpatterns = [
    path('business/', views.facebook_business, name='facebookbusiness'),
]