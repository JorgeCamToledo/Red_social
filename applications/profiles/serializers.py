from rest_framework import serializers
from applications.profiles.models import Profile
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'first_name', 'last_name','email']
        
class ViewProfileSerialier(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Profile
        fields = '__all__'

class ChangeProfilePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['image_profile']
        
class ChangeCoverPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['image_cover']
        
class ChangPrivacySerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['is_public']
        
    def update(self, instance, validated_data):
        instance.is_public = not instance.is_public
        instance.save()
        return instance