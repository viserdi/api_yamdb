from django.db.models import Avg
from rest_framework import exceptions, serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description',
                  'genre', 'category', 'rating')
        read_only_fields = ('id',)

    def get_rating(self, obj):
        try:
            rating = obj.reviews.aggregate(Avg('score'))
            return rating.get('score__avg')
        except TypeError:
            return None


class CreateTitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class CreateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=(
            UniqueValidator(
                queryset=User.objects.all(),
                message='Данный e-mail уже существует!'
            ),
        )
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        read_only_fields = ('role', )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать username "me"'
            )
        return value


class CreateAdminSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=(
            UniqueValidator(
                queryset=User.objects.all(),
                message='Данный e-mail уже существует!'
            ),
        )
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать username "me"'
            )
        return value


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=200,
        required=True
    )
    confirmation_code = serializers.CharField(
        max_length=200,
        required=True
    )

    def validate_username(self, name):
        if name == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать username "me"'
            )
        if not User.objects.filter(username=name).exists():
            raise exceptions.NotFound('Такого пользователя не существует')
        return name
