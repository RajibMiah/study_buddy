from django.urls import path
from rest_framework.authtoken import views

from chat.views.auth_view import *
from chat.views.call_view import EndCall, StartCall
from chat.views.message_view import MessageView

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),
    path('login/', Login.as_view(), name='login'),
    path('registration/', RegisterView.as_view()),
    path('logout/', LogOutView.as_view()),
    path('users/', UsersView.as_view()),
    path('message/', MessageView.as_view()),
    path('start-call/', StartCall.as_view()),
    path('end-call/', EndCall.as_view()),
    path('test-socket/', test_socket)
]
