from api import permissions
from api.serializers import (CreateAdminSerializer, CreateUserSerializer,
                             GetTokenSerializer)
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb.settings import FROM_EMAIL

from .models import User


def send_email_with_code(username, email):
    """
    Созданиие и отправка кода подтверждения на указанную почту.
    """
    user = get_object_or_404(User, username=username)
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Код подтверждения',
        message=f'Ваш код {confirmation_code}',
        from_email=FROM_EMAIL,
        recipient_list=[email]
    )


class APISignUp(APIView):
    """
    Создание пользователя с уникальными полями username и email,
    отправка кода подтверждения на указанную почту.
    """
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            send_email_with_code(
                serializer.data['username'],
                serializer.data['email']
            )
            return Response(
                {'email': serializer.data['email'],
                 'username': serializer.data['username']},
                status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIGetToken(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(
                User, username=serializer.data['username'])
            if default_token_generator.check_token(
               user, serializer.data['confirmation_code']):
                token = AccessToken.for_user(user)
                return Response(
                    {'token': str(token)}, status=status.HTTP_200_OK)
            return Response({
                'confirmation code': 'Некорректный код подтверждения!'},
                status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIUser(APIView):
    """
    Получение и изменение данных своей учетной записи,
    доступно всем зарегистрированным пользователям.
    """
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=request.user.username)
        serializer = CreateUserSerializer(user, many=False)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=request.user.username)
        serializer = CreateUserSerializer(
            user, data=request.data, partial=True, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSetForAdmin(ModelViewSet):
    """
    Управление всеми учетными данными пользоваталей,
    доступно только администратору.
    """
    queryset = User.objects.all()
    serializer_class = CreateAdminSerializer
    lookup_field = 'username'
    permission_classes = (permissions.IsAdmin, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username', )
