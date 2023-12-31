from rest_framework import serializers
from applications.posts.models import Post
from applications.comments.models import Comment
from applications.reactions.models import Reaction
from django.conf import settings


class GetPostsSerializer(serializers.ModelSerializer):
    comment_count = serializers.SerializerMethodField()
    reaction_count = serializers.SerializerMethodField()
    view_comments = serializers.SerializerMethodField()
    view_people_who_react = serializers.SerializerMethodField()

    def get_comment_count(self, post):
        return Comment.objects.filter(post=post).count()

    def get_reaction_count(self, post):
        return Reaction.objects.filter(post=post).count()
    
    def get_view_comments(self,post):
        return f'{settings.COMMENT_API_URL}{post.id}/'
    def get_view_people_who_react(self,post):
        return f'{settings.REACTION_API_URL}{post.id}/'
    
    class Meta:
        model = Post
        fields = ['id', 'images', 'descripcion', 'created_at', 'comment_count', 'reaction_count','view_comments','view_people_who_react','user']
        
        
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'