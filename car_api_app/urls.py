from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, include
from .views import UserViewSet, UserCarViewSet, CarModelViewSet, CarBrandViewSet

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
    # path('/', include(router.urls)),
]
