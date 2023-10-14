from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from applications.comments.serializers import CommentSerializer
from applications.profiles.models import Profile
from applications.posts.models import Post
from applications.followers.models import Follower
from applications.comments.models import Comment
from applications.reactions.serializers import ReactionSerializer
from applications.reactions.models import Reaction


class ReactionList(APIView):
        
    def post(self, request):
        print(request.user)
        request.data['user'] = request.user.id
        try:
            post = Post.objects.get(id=request.data['post'])
        except Post.DoesNotExist:
            return Response("No se encontró la publicación", status=status.HTTP_400_BAD_REQUEST)
        profile_who_post = Profile.get_profile(user = post.user)
        privacity = profile_who_post.is_public
        # Verificar si el usuario ya ha reaccionado a esta publicación
        existing_reaction = Reaction.objects.filter(user=request.user, post=post).first()

        if existing_reaction:
            # Si ya ha reaccionado, actualiza la reacción si es diferente
            if existing_reaction.type != request.data['type']:
                existing_reaction.type = request.data['type']
                existing_reaction.save()
                serializer = ReactionSerializer(existing_reaction)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response("Ya has reaccionado de esta manera a esta publicación", status=status.HTTP_400_BAD_REQUEST)
        else:
            # Si no ha reaccionado previamente, crea una nueva reacción
            serializer = ReactionSerializer(data=request.data)
            if serializer.is_valid():
                if request.user == profile_who_post.user or Follower.is_follower(request.user, profile_who_post.user):
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                if not privacity:
                    return Response("Este perfil es privado, primero debes seguir a este usuario", status=status.HTTP_204_NO_CONTENT)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
class ListReactionsByPost(APIView):
    def get(self, request, pk,):
        post = Post.objects.get(id = pk)
        profile_who_post = Profile.get_profile(user = post.user)
        privacity = profile_who_post.is_public
        queryset = Reaction.objects.filter(post = pk).order_by('id')
        serializer = ReactionSerializer(queryset, many=True, context={'request':request})
        if request.user == profile_who_post.user or Follower.is_follower(request.user, profile_who_post.user):
            return Response(serializer.data,status=200)
        if not privacity:
                    return Response("Este perfil es privado, primero debes seguir a este usuario", status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.data,status=200)