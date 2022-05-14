from django_filters import rest_framework as djfilt
from car_api_app.models import CarModel, CarBrand


# Filters
class CarModelFilter(djfilt.FilterSet):
    name_search = djfilt.CharFilter(field_name="name", lookup_expr='contains')

    class Meta:
        model = CarModel
        fields = ['name_search']


class CarBrandFilter(djfilt.FilterSet):
    name_search = djfilt.CharFilter(field_name="name", lookup_expr='contains')

    class Meta:
        model = CarBrand
        fields = ['name_search']
