from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TitleViewSet, CategoryViewSet, ReviewViewSet, GenreViewSet, CommentViewSet

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

urlpatterns = [
    path('', include(router_v1.urls)),
]
