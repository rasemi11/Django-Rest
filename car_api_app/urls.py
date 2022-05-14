from rest_framework import routers, serializers, viewsets
from car_api_app.models import AppUser, CarModel, CarBrand, UserCar
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django_filters import rest_framework as djfilt
from django.urls import path, include



# Serializers
class CarBrandSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = CarBrand
        fields = '__all__'

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(CarBrandSerializer, self).get_field_names(declared_fields, info)
        return expanded_fields


class CarModelSerializer(serializers.HyperlinkedModelSerializer):
    car_brand = CarBrandSerializer()

    class Meta:
        model = CarModel
        fields = '__all__'

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(CarModelSerializer, self).get_field_names(declared_fields, info)
        return expanded_fields

    def create(self, validated_data):
        brand_name = validated_data.pop('car_brand')['name']
        car_brand = CarBrand.objects.filter(name=brand_name)
        if len(car_brand) < 1:
            car_brand = CarBrand.objects.create(name=brand_name)
        validated_data['car_brand'] = car_brand
        instance = CarModel.objects.create(**validated_data)
        return instance


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AppUser
        fields = '__all__'
        lookup_field = 'name'

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(UserSerializer, self).get_field_names(declared_fields, info)
        return expanded_fields


class UserCarSerializer(serializers.HyperlinkedModelSerializer):
    car_model = CarModelSerializer()
    user = UserSerializer()

    class Meta:
        model = UserCar
        fields = '__all__'
        # lookup_field = 'user'

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(UserCarSerializer, self).get_field_names(declared_fields, info)
        return expanded_fields


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


# ViewSets
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AppUser.objects.all()
    serializer_class = UserSerializer


class UserCarViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserCar.objects.all()
    serializer_class = UserCarSerializer


class CarModelViewSet(viewsets.ModelViewSet):
    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer
    filter_backends = (djfilt.DjangoFilterBackend,)
    filterset_class = CarModelFilter


class CarBrandViewSet(viewsets.ModelViewSet):
    queryset = CarBrand.objects.all()
    serializer_class = CarBrandSerializer
    filter_backends = (djfilt.DjangoFilterBackend,)
    filterset_class = CarBrandFilter


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'user_car', UserCarViewSet)
router.register(r'car_model', CarModelViewSet)
router.register(r'car_brand', CarBrandViewSet)


schema_view = get_schema_view(
    openapi.Info(
        title="Car API",
        default_version='v1',
        description="Test description",
    ),
    public=True,
)

urlpatterns = [
]
