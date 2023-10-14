from rest_framework import serializers
from applications.follow_request.models import FollowRequest

class FollowRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowRequest
        fields = '__all__'
