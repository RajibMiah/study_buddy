from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("register/", views.registerPage, name="register"),
    path("topics/", views.topicsPage, name="topics"),
    path("activity/", views.activityPage, name="activity"),
    path("profile/<int:pk>/", views.userProfile, name="user-profile"),
    path("account/edit/", views.updateUser, name="update-user"),
    path("room/<int:pk>/", views.room, name="room"),
    path("room/create/", views.createRoom, name="create-room"),
    path("room/<int:pk>/edit/", views.updateRoom, name="update-room"),
    path("room/<int:pk>/delete/", views.deleteRoom, name="delete-room"),
    path("message/<int:pk>/delete/", views.deleteMessage, name="delete-message"),
    path("api/", include("base.api.urls")),
]
