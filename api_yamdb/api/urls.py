from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import *

router_v1 = DefaultRouter()
router_v1.register('titles', TitleViewSet, basename='title')
router_v1.register('categories', CategoryViewSet,
                   basename='category')
router_v1.register('genres', GenreViewSet, basename='genre')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
