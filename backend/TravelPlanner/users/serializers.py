from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model 
 
User=get_user_model()

class LoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField()

    def to_representation(self, instance):
        ret=super().to_representation(instance)
        ret.pop('password', None)
        return ret

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id', 'email', 'username', 'password')
        extra_kwargs={'password':{'write_only':True}}

    def create(self,validated_data):
        user=User.objects.create_user(**validated_data)
        return user
    
from rest_framework import serializers
from .models import Place

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ['id', 'name', 'order', 'visited', 'trip', 'image_url']
        extra_kwargs = {
            'order': {'required': False},
        }

class TripSerializer(serializers.ModelSerializer):
    places = PlaceSerializer(many=True, read_only=True)

    class Meta:
        model = Trip
        fields = ['id', 'starting_date', 'place', 'number_of_days', 'places', 'image_url']

# serializers.py

