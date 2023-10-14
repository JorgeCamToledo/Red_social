from rest_framework import serializers
from applications.comments.models import Comment
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
        fields = ['username', 'first_name', 'last_name', 'profile']

    
class GetCommentsSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Incluye los datos del usuario en el comentario

    class Meta:
        model = Comment
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'