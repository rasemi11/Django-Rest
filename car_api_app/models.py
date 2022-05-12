from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime


class SoftDeleteManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class SoftDeleteModel(models.Model):

    objects = SoftDeleteManager()
    all_objects = models.Manager()
    deleted_at = models.DateTimeField(null=True, blank=True, default=None)

    def soft_delete(self):
        self.deleted_at = datetime.now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()

    class Meta:
        abstract = True


class AppUser(AbstractUser):

    name = models.CharField(max_length=100, unique=True)
    mobile_number = models.CharField(max_length=10, unique=True)
    birth_date = models.DateField(null=True, blank=True)

    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class CarBrand(SoftDeleteModel):

    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name


class CarModel(SoftDeleteModel):

    car_brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.car_brand} {self.name}'


class UserCar(SoftDeleteModel):

    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    first_reg = models.DateTimeField()
    odometer = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f'{self.user} {self.car_model}'
