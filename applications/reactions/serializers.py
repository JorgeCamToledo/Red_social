from rest_framework import serializers
from applications.reactions.models import Reaction
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

    
class GetReactionSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Incluye los datos del usuario en el comentario

    class Meta:
        model = Reaction
        fields = '__all__'

class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = '__all__'