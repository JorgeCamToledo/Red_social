from rest_framework import serializers
from applications.reactions.models import Reaction


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = '__all__'