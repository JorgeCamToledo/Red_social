from rest_framework import serializers
from applications.comments.models import Comment 


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'