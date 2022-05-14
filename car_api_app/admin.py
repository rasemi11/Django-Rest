from django.contrib import admin
from car_api_app.models import CarModel, CarBrand, UserCar, AppUser

admin.site.register(CarModel)
admin.site.register(CarBrand)
admin.site.register(UserCar)
admin.site.register(AppUser)
