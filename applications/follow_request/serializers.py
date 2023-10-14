from rest_framework import serializers
from applications.follow_request.models import FollowRequest
from applications.profiles.models import Profile
from django.contrib.auth.models import User

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['image_profile']  # Agrega el campo de la imagen del perfil

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(source='detalles_usuario', required=False)

    class Meta:
        model = User
        fields = ['username','profile']

class GetFollowRequestSerializer(serializers.ModelSerializer):
    receiver = UserSerializer()
    requester = UserSerializer()
    class Meta:
        model = FollowRequest
        fields = '__all__'

class FollowRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowRequest
        fields = '__all__'
