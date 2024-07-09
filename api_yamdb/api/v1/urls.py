"""
API URLS
"""
from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (CustomUserModelViewSet,
                    custom_user_signup,
                    CustomUserTokenView,
                    CategoryViewSet,
                    GenreViewSet,
                    TitleViewSet,
                    CommentViewSet,
                    ReviewViewSet)

app_name = 'api'

router_v1 = SimpleRouter()

# YaMDb API v.1

router_v1.register('users', CustomUserModelViewSet, basename='users')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register(r"titles/(?P<title_id>\d+)/reviews",
                   ReviewViewSet, basename='reviews')
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet, basename='comments')

v1_auth = [
    path('signup/', custom_user_signup, name='user_signup'),

    path('token/', CustomUserTokenView.as_view(),
         name='token_obtain_pair'),
]

v1 = [
    path('auth/', include(v1_auth)),

    path('', include(router_v1.urls)),
]

urlpatterns = [
    path('', include(v1)),
]
