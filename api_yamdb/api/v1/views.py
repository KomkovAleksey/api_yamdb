"""
API views
"""
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination

from reviews.models import Category, Genre, Title, Review
from users.models import CustomUser
from .filters import TitleFilter
from .mixins import ModelMixinViewSet
from .permissions import (IsAdminUserOrReadOnly,
                          CustomUserIsAdminBasePermission,
                          IsAdminOrModeratorOrAuthor)
from .serializers import (CategorySerializer,
                          GenreSerializer,
                          TitleReadSerializer,
                          TitleWriteSerializer,
                          CustomUserSignupSerializer,
                          CustomUserTokenSerializer,
                          CustomUserDetailSerializer,
                          CustomUserModelSerializer,
                          CommentSerializer,
                          ReviewSerializer)


class CategoryViewSet(ModelMixinViewSet):
    """Viewset for categories."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]
    filter_backends = (SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'


class GenreViewSet(ModelMixinViewSet):
    """Viewset for genres."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(ModelViewSet):
    """Viewset for titles"""

    queryset = Title.objects.all()
    permission_classes = [IsAdminUserOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        avg = Review.objects.filter(title=instance).aggregate(Avg('score'))
        instance.rating = avg['score__avg']
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для обработки отзывов."""

    permission_classes = [IsAdminOrModeratorOrAuthor]
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    serializer_class = ReviewSerializer

    def title_query(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.title_query())


class CommentViewSet(ReviewViewSet):
    """Вьюсет для обработки комментариев."""

    serializer_class = CommentSerializer

    def review_query(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.review_query())


@api_view(['POST'])
@permission_classes([AllowAny])
def custom_user_signup(request):
    """
    View function for
    getting verification code
    for CustomUser signup
    """
    serializer = CustomUserSignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    email = serializer.validated_data.get('email')

    user, created = CustomUser.objects.get_or_create(
        username=username,
        email=email, )

    if not created:
        user.confirmation_code = default_token_generator.make_token(user)
        user.save(update_fields=['confirmation_code'])
    else:
        user.confirmation_code = default_token_generator.make_token(user)
        user.save()

    send_mail(
        subject='Your confirmation code for YaMDb',
        message=f'Your confirmation code: {user.confirmation_code}.',
        from_email='admin@yamdb.ru',
        recipient_list=[email, ],
        fail_silently=True,
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


class CustomUserTokenView(APIView):
    """
    APIView class for
    getting access token
    for CustomUser authentication
    """
    serializer_class = CustomUserTokenSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')

        user = CustomUser.objects.get(
            username=username)

        refresh = RefreshToken.for_user(user)
        return Response({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        }, status=status.HTTP_200_OK)


class CustomUserModelViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet class for
    getting, posting, updating, deleting
    of CustomUsers
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserModelSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    permission_classes = (CustomUserIsAdminBasePermission,)

    @action(detail=False,
            methods=['get', 'patch'],
            permission_classes=[IsAuthenticated, ])
    def me(self, request):
        if request.method == 'GET':
            serializer = CustomUserDetailSerializer(instance=request.user)
        if request.method == 'PATCH':
            serializer = CustomUserDetailSerializer(
                data=request.data, instance=request.user)
            serializer.is_valid(raise_exception=True)
            serializer.save(username=request.user.username,
                            email=request.user.email,
                            role=request.user.role)

        return Response(serializer.data, status=status.HTTP_200_OK)
