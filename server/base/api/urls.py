from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register(r'room', views.RoomModelViewSet, basename='room-details')
router.register(r'topic', views.TopicsModelViewSet, basename='topics')
router.register(r'profile', views.UserProfileModelViewSet,
                basename='user-profile')
router.register(r'edit-profile', views.UserEditProfileModelViewSet,
                basename='user-profile')
router.register(r'votes', views.VoteModelViewSet, basename='votes')
router.register(r'userfollowing', views.UserFollowingModelViewSet,
                basename='userfollowing')

router.register(r'most-followed-peoples',
                views.MostFollowedPeopleModelViewSet, basename='most-followed-people')

urlpatterns = [

] + router.urls
