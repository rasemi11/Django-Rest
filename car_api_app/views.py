from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from .forms import AppUserForm
from django.urls import reverse_lazy
from django.views import generic
from car_api_app.models import AppUser, CarModel, CarBrand, UserCar
from .serializers import UserSerializer, UserCarSerializer, CarModelSerializer, CarBrandSerializer
from .filters import CarModelFilter, CarBrandFilter
from rest_framework import viewsets
from django_filters import rest_framework as djfilt


class ProtectedView(TemplateView):
    template_name = 'base.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProtectedView, self).dispatch(*args, **kwargs)


class SignUpView(generic.CreateView):
    form_class = AppUserForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


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
