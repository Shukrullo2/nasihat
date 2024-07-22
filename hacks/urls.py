from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

urlpatterns = [
    path('hacks/', views.getHacks, name="hacks"),
    path('top-hacks/', views.getTopHacks, name="top-hacks"),
    path('new-hacks/', views.getNewHacks, name="new-hacks"),
    path('hot-hacks/', views.getHotHacks, name="hot-hacks"),
    path('hack/<str:pk>', views.getHack, name="hack"),

    path('writers/', views.getWriters, name="writers"),
    path('comments/', views.getComments, name="comments"),
    path('replies/', views.getReplies, name="replies"),
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('create-hack/', views.createHack, name="create-hack"),
    path('create-comment/', views.createComment, name="create-comment"),
    path('create-reply/', views.createReply, name="create-reply"),
    path('create-report/', views.createReport, name="create-report"),

    path('upvote/', views.upVote, name="upvote"),
    path('downvote/', views.downVote, name="downvote"),
    ]

