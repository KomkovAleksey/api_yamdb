from rest_framework import mixins, viewsets


class ModelMixinViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                        mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """Custom viewset for genres and categories"""

    pass
