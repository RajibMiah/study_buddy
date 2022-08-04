from django.urls import path

from . import views

getRooms_details = views.GetRooms.as_view({
    'get': 'retrieve',
    'post': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


urlpatterns = [
    path('',  views.getRoutes),
    path('rooms/', getRooms_details),
    path('topics/', views.getTopics),
    path('profile/', views.UserProfile.as_view(), name='user-profile')
    # path('rooms/<str:pk>/', views.getRoom),

]
