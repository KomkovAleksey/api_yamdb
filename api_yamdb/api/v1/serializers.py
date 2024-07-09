"""
API serializers
"""
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework import serializers

from reviews.models import Category, Genre, Title, Comment, Review
from users.models import CustomUser
from .validators import validate_data


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for reviews."""
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == 'POST'
            and Review.objects.filter(title=title, author=author).exists()
        ):
            raise ValidationError(
                'Больше одного отзыва писать нельзя'
            )
        return data

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for comments."""
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for model Category."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Serializer for model Genre."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    """Serializer for model Title on GET requests."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')


class TitleWriteSerializer(serializers.ModelSerializer):
    """Serializer for model Title on POST, PATCH, DELETE requests."""

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


class CustomUserSignupSerializer(serializers.Serializer):
    """
    CustomUser signup serializer
    """
    email = serializers.EmailField(max_length=254)
    username = serializers.CharField(max_length=150)

    def validate(self, data):
        return validate_data(data)


class CustomUserTokenSerializer(serializers.Serializer):
    """
    CustomUser token serializer
    """
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(max_length=64, required=True)

    def validate(self, data):
        if not CustomUser.objects.filter(
                username__iexact=data['username']).exists():
            raise Http404('User not found')

        if (CustomUser.objects
                .get(username__iexact=data['username'])
                .confirmation_code != data.get('confirmation_code')):
            raise serializers.ValidationError('Check confirmation code')
        return data


class CustomUserDetailSerializer(serializers.Serializer):
    """
    CustomUser detail serializer
    """
    username = serializers.CharField(max_length=150, required=False)
    email = serializers.EmailField(max_length=254, required=False)
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    bio = serializers.CharField(required=False)
    role = serializers.CharField(required=False)

    def validate(self, data):
        return validate_data(data)

    def update(self, instance, validated_data):
        instance.username = validated_data['username']
        instance.email = validated_data['email']
        if 'first_name' in validated_data:
            instance.first_name = validated_data['first_name']
        if 'last_name' in validated_data:
            instance.last_name = validated_data['last_name']
        if 'bio' in validated_data:
            instance.bio = validated_data['bio']
        if 'role' in validated_data:
            instance.role = validated_data['role']
        instance.save()
        return instance


class CustomUserModelSerializer(serializers.ModelSerializer):
    """
    Custom user ModelSerializer
    """
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.CharField(max_length=150, required=True)

    class Meta:
        model = CustomUser
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role')

    def validate(self, data):
        return validate_data(data)
