from rest_framework import serializers
from car_api_app.models import AppUser, CarModel, CarBrand, UserCar


# Serializers
class CarBrandSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = CarBrand
        fields = '__all__'

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(CarBrandSerializer, self).get_field_names(declared_fields, info)
        return expanded_fields

    def create(self, validated_data):
        instance = CarBrand.objects.create(**validated_data)
        return instance


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

    def create(self, validated_data):
        instance = CarBrand.objects.create(**validated_data)
        return instance


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

    def create(self, validated_data):
        brand_name = validated_data.pop('car_brand')['name']
        car_brand = CarBrand.objects.filter(name=brand_name)
        if len(car_brand) < 1:
            car_brand = CarBrand.objects.create(name=brand_name)
        validated_data['car_brand'] = car_brand
        instance = CarModel.objects.create(**validated_data)
        return instance

    def to_representation(self, instance):
        self.fields['car_model'] = CarModelSerializer()
        self.fields['user'] = UserSerializer()
        return super(UserCarSerializer, self).to_representation(instance)
