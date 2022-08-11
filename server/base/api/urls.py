from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register(r'room', views.RoomModelViewSet, basename='room-details')
router.register(r'topic', views.TopicsModelViewSet, basename='topics')
router.register(r'profile', views.UserProfileModelViewSet,
                basename='user-profile')
router.register(r'votes', views.VoteModelViewSet, basename='votes')


urlpatterns = [
    # path('',  views.getRoutes),

] + router.urls
