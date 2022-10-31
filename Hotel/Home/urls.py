from urllib.parse import urlparse
from django.urls import path
from . views import *
urlpatterns = [
    path('',home,name='home'),

    path('chech_booking',chech_booking,name='chech_booking'),
    
    path('login/',login_page,name='login'),
    
    path('regester/',regester_page,name='regester'),

    path('hotel-detail/<uid>/',hotel_detail,name='hotel-detail'),

    path('logout',logout_user, name='logout_user')

]
