import django_filters

from reviews.models import Title


class TitleFilter(django_filters.FilterSet):
    """Filter for Titles"""

    category = django_filters.CharFilter(
        field_name='category__slug',
    )
    genre = django_filters.CharFilter(
        field_name='genre__slug',
    )
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )
    year = django_filters.NumberFilter(
        field_name='year',
    )

    class Meta:
        model = Title
        fields = ('name', 'year', 'category', 'genre')
