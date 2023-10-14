from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from applications.posts.serializers import PostSerializer,GetPostsSerializer
from applications.posts.models import Post
from applications.followers.models import Follower
from applications.profiles.models import Profile


class PostList(APIView):

    def post(self,request):
        request.data['user'] = request.user.id
        serializer=PostSerializer(data=request.data)
        if serializer.is_valid():
            # asignar el usuario autenticado a la instancia de Post
            serializer.save()
            serializer_response = serializer.data
            return Response(serializer_response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class UserPostsList(APIView):
    def get(self,request,pk):
        print(request.user)
        profile = Profile.get_profile(pk)
        if profile !=0:
            privacity = profile.is_public
            queryset = Post.objects.filter(user = pk).order_by('created_at')
            serializer = GetPostsSerializer(queryset, many=True, context={'request':request})
            if request.user == profile.user or Follower.is_follower(request.user, profile.user):
                    return Response(serializer.data, status=status.HTTP_200_OK)
            if not privacity:
                    return Response("Este perfil es privado, primero debes seguir a este usuario", status=status.HTTP_204_NO_CONTENT)
            return Response(serializer.data,status=200)
        return Response("No se encontro el perfil del usuario", status=status.HTTP_204_NO_CONTENT)
    
class PostByFollowedUsers(APIView):
    def get(self, request):
        user = request.user

        # Obtén los usuarios que sigues
        following_users = Follower.objects.filter(follower=user).values_list('followed', flat=True)

        # Obtén los perfiles de los usuarios que sigues
        following_profiles = Profile.objects.filter(user__in=following_users)

        # Ahora, `following_profiles` contiene los perfiles de los usuarios a los que sigues
        
        queryset = Post.objects.filter(user__detalles_usuario__in=following_profiles).order_by('-created_at')

        # Modifica los resultados para asignar el username al campo user
        posts_with_username = [
            {"id": post.id, "images": post.images.url, "descripcion": post.descripcion, "created_at": post.created_at, "user": post.user.username}
            for post in queryset
        ]

        # Envía la respuesta con los datos modificados
        return Response(posts_with_username, status=status.HTTP_200_OK)