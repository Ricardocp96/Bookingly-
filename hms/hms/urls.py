
from django.contrib import admin
from django.urls import path
from hospital.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage, name='homepage'),
    path('about/', aboutpage, name='aboutpage'),
    path('createaccount/', createaccount, name='createaccount'),
    path('login/', loginpage, name='loginpage'),
    path('logout/', Logout, name='logout'),
    path('home/', Home, name='home'),
    path('profile/', profile, name='profile'),
    path('makeappointments/', MakeAppointments, name='makeappointments'),
    path('viewappointments/', viewappointments, name='viewappointments'),
]
