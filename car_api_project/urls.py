"""car_api_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers, serializers, viewsets
from car_api_app.models import AppUser, CarModel, CarBrand, UserCar
from django.views.generic.base import TemplateView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django_filters import rest_framework as djfilt
from car_api_app.views import SignUpView


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
    car_model = serializers.HyperlinkedRelatedField(view_name='car_model', queryset=CarModel.objects.all())
    user = serializers.HyperlinkedRelatedField(view_name='users', queryset=AppUser.objects.all())

    class Meta:
        model = UserCar
        fields = '__all__'
        lookup_field = 'user'

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(UserCarSerializer, self).get_field_names(declared_fields, info)
        return expanded_fields


# Filters
class CarModelFilter(djfilt.FilterSet):
    name_search = djfilt.CharFilter(field_name="name", lookup_expr='contains')

    class Meta:
        model = CarModel
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


router = routers.DefaultRouter()
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
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path("accounts/signup/", SignUpView.as_view(), name="signup"),
    path("accounts/", include("django.contrib.auth.urls")),
    path(r'swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
