
from django.urls import include, path

from .views import *

urlpatterns = [

    path('', home, name="shop-home"),
    path('course/<slug>', view_course, name="shop-course"),
    path('become_pro/', become_pro, name="become_pro"),
    path('charge/', charge, name="charge"),
    # path('login/'  , login_attempt , name="login"),
    # path('register/'  , register , name="register"),
    # path('logout_attempt/' , logout_attempt , name="logout")


]
