from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import APIGetToken, APISignUp, APIUser, UserViewSetForAdmin

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet)

router_v1 = DefaultRouter()
router_v1.register('titles', TitleViewSet, basename='title')
router_v1.register('categories', CategoryViewSet,
                   basename='category')
router_v1.register('genres', GenreViewSet, basename='genre')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
                   basename='reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)
router_v1.register('users', UserViewSetForAdmin, basename='users')

urlpatterns = [
    path('auth/signup/', APISignUp.as_view(), name='signup'),
    path('auth/token/', APIGetToken.as_view(), name='token'),
    path('users/me/', APIUser.as_view(), name='me'),
    path('', include(router_v1.urls)),
]
