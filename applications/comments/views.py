from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from applications.comments.serializerz import CommentSerializer
from applications.profiles.models import Profile
from applications.posts.models import Post
from applications.followers.models import Follower
from applications.comments.models import Comment


class CommentList(APIView):
        
    def post(self,request):
        request.data['user'] = request.user.id
        post = Post.objects.get(id = request.data['post'])
        profile_who_post = Profile.get_profile(user = post.user)
        privacity = profile_who_post.is_public
        serializer=CommentSerializer(data=request.data)
        if serializer.is_valid():
            if request.user == profile_who_post.user or Follower.is_follower(request.user, profile_who_post.user):
                serializer.save()
                serializer_response = serializer.data
                return Response(serializer_response, status=status.HTTP_201_CREATED)
            if not privacity:
                    return Response("Este perfil es privado, primero debes seguir a este usuario", status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class ListCommentsByPost(APIView):
    def get(self, request, pk,):
        post = Post.objects.get(id = pk)
        profile_who_post = Profile.get_profile(user = post.user)
        privacity = profile_who_post.is_public
        queryset = Comment.objects.filter(post = pk).order_by('id')
        serializer = CommentSerializer(queryset, many=True, context={'request':request})
        if request.user == profile_who_post.user or Follower.is_follower(request.user, profile_who_post.user):
            return Response(serializer.data,status=200)
        if not privacity:
                    return Response("Este perfil es privado, primero debes seguir a este usuario", status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.data,status=200)
    