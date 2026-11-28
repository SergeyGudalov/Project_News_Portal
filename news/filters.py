import django_filters
from django.forms import DateInput
from .models import Post


class PostFilter(django_filters.FilterSet):
    author = django_filters.CharFilter(
        field_name='author__user__first_name',
        lookup_expr='icontains',
        label='Имя автора'
    )

    created_at = django_filters.DateFilter(
        lookup_expr='date__gt',
        label='Опубликовано после',
        widget=DateInput(attrs={'type': 'date'})
    )

    title = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Заголовок'
    )
    class Meta:
        model = Post
        fields = []
