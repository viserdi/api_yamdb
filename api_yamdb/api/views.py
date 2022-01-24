from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination

from reviews.models import Category, Genre, Review, Title

from .filters import TitleGenreFilter
from .mixins import ListCreateDestroyViewSet
from .permissions import IsAdminOrReadOnly, IsAuthorOrAdminOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          CreateTitleSerializer, GenreSerializer,
                          ReviewSerializer, TitleSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    """
    Управление произведениями доступно только админу,
    остальные пользователи в режиме read only.
    """
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleGenreFilter

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return CreateTitleSerializer
        return TitleSerializer


class CategoryViewSet(ListCreateDestroyViewSet):
    """
    Управление категориями доступно только админу,
    остальные пользователи в режиме read only.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)


class GenreViewSet(ListCreateDestroyViewSet):
    """
    Управление жанрами доступно только админу,
    остальные порльзователи в режиме read only.
    """
    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Управление всеми отзывами доступно только админу и модератору,
    остальные пользователи могут управлять только своими отзывами.
    """
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrAdminOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        if Review.objects.filter(author=self.request.user,
                                 title=title).exists():
            raise ValidationError('Нельзя оставлять больше одного отзыва!')
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Управление всеми комментариями доступно только админу и модератору,
    остальные пользователи могут управлять только своими комментариями.
    """
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrAdminOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'),
                                   title_id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, review=review)
