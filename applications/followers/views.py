from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from applications.followers.models import Follower
from applications.profiles.models import Profile
from applications.follow_request.models import FollowRequest

class FollowView(APIView):
    def get_user(self, pk):
        try:
            return User.objects.get(id = pk) 
        except User.DoesNotExist:
            return 0
    def get_profile(self, user):
        try:
            return Profile.objects.get(user = user) 
        except Profile.DoesNotExist:
            return 0
    
    def post(self,request):
        user_to_follow = self.get_user(request.data['user'])
        
        if not user_to_follow:
            return Response("No se encontro el perfil del usuario", status=status.HTTP_204_NO_CONTENT)
        
        profile_user_to_follow = self.get_profile(user = user_to_follow.id)
        privacity =profile_user_to_follow.is_public
        
        if user_to_follow == request.user:
            return Response({"error": "No puedes seguirte a ti mismo."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not privacity:
            follow_request, created = FollowRequest.objects.get_or_create(requester=request.user, receiver = user_to_follow)
            if created:
                return Response("Solicitud de seguimiento enviada. Espera a que el usuario confirme.", status=status.HTTP_200_OK)
            else:
                return Response("Ya has enviado una solicitud de seguimiento a este usuario previamente.", status=status.HTTP_200_OK)
        
        follower, created = Follower.objects.get_or_create(follower=request.user, followed=user_to_follow)
        if created:
            return Response({"message": f"Siguiendo a {user_to_follow.username}"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": f"Ya estás siguiendo a {user_to_follow.username}"}, status=status.HTTP_200_OK)
    
    def get(self, request):
        user = request.user
        followers = user.followers.all()
        following = user.following.all()

        followers_usernames = [follower.follower.username for follower in followers]
        following_usernames = [followed.followed.username for followed in following]

        data = {
            "followers": followers_usernames,
            "following": following_usernames
        }

        return Response(data, status=status.HTTP_200_OK)