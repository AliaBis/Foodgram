from django.urls import include, path
from djoser.views import TokenCreateView, TokenDestroyView
from rest_framework.routers import DefaultRouter
from users.views import CustomUserViewSet, FollowListView, FollowViewSet

app_name = 'users'

router = DefaultRouter()

router.register('users', CustomUserViewSet, basename='users')


urlpatterns = [
    path('users/<int:user_id>/subscribe/', FollowViewSet.as_view(),
         name='follow'),
    path('users/subscriptions/', FollowListView.as_view(),
         name='subsciptions'),
    path('', include(router.urls)),
    path('auth/token/login/',
         TokenCreateView.as_view(),
         name='login'),
    path('auth/token/logout/',
         TokenDestroyView.as_view(),
         name='logout'),
]
