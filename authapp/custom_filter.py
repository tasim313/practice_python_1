from django_filters import rest_framework as filters
# from rest_framework import filters

from .models import User


class UserFilter(filters.FilterSet):
    email = filters.CharFilter(lookup_expr='icontains')
    username = filters.CharFilter(lookup_expr='icontains')
    # profiles__providers = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = User
        fields = ('username',)


# class CustomSearchFilter(filters.SearchFilter):

#     def get_search_fields(self, view, request):
#         if request.get_queryset.get('email', 'username'):
#             return ['email', 'username']
#         return super(CustomSearchFilter, self).get_search_fields(view, request)
