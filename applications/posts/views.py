from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from applications.posts.serializers import PostSerializer
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
    def is_follower(self, follower, profile_user):
        return Follower.objects.filter(follower=follower, followed=profile_user).exists()
    
    def get_profile(self, user):
        try:
            return Profile.objects.get(user = user) 
        except Profile.DoesNotExist:
            return 0
    
    def get(self,request,pk):
        print(request.user)
        profile = self.get_profile(pk)
        if profile !=0:
            privacity = profile.is_public
            queryset = Post.objects.filter(user = pk).order_by('created_at')
            serializer = PostSerializer(queryset, many=True, context={'request':request})
            if request.user == profile.user or self.is_follower(request.user, profile.user):
                    return Response(serializer.data, status=status.HTTP_200_OK)
            if not privacity:
                    return Response("Este perfil es privado, primero debes seguir a este usuario", status=status.HTTP_204_NO_CONTENT)
            return Response(serializer.data,status=200)
        return Response("No se encontro el perfil del usuario", status=status.HTTP_204_NO_CONTENT)