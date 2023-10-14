from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from applications.followers.models import Follower
from applications.profiles.models import Profile
from applications.follow_request.models import FollowRequest
from applications.history.models import History
from utils.exceptions import ExcepcionPersonalizada

class FollowView(APIView):
    def get_user(self, pk):
        try:
            return User.objects.get(id = pk) 
        except User.DoesNotExist:
            return 0
    
    def post(self,request):
        try:
            user_to_follow = self.get_user(request.data['user'])
            
            if not user_to_follow:
                raise ExcepcionPersonalizada("No se encontro el perfil del usuario", status=status.HTTP_204_NO_CONTENT)
            
            profile_user_to_follow = Profile.get_profile(user = user_to_follow.id)
            privacity =profile_user_to_follow.is_public
            
            if user_to_follow == request.user:
                raise ExcepcionPersonalizada("No puedes seguirte a ti mismo.", status=status.HTTP_400_BAD_REQUEST)
            
            if not privacity:
                follow_request, created = FollowRequest.objects.get_or_create(requester=request.user, receiver = user_to_follow)
                if created:
                    history_entry = History(username=request.user.username, event=f'Se envio una solicitud de seguimiento a {user_to_follow.username}')
                    history_entry.save()
                    return Response({"message":"Solicitud de seguimiento enviada. Espera a que el usuario confirme."}, status=status.HTTP_200_OK)
                else:
                    return Response({"message":"Ya has enviado una solicitud de seguimiento a este usuario previamente."}, status=status.HTTP_200_OK)
            
            follower, created = Follower.objects.get_or_create(follower=request.user, followed=user_to_follow)
            if created:
                history_entry = History(username=request.user.username, event=f'Empezo a seguir {user_to_follow.username}')
                history_entry.save()
                return Response({"message": f"Siguiendo a {user_to_follow.username}"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": f"Ya estás siguiendo a {user_to_follow.username}"}, status=status.HTTP_200_OK)
        except ExcepcionPersonalizada as e:
            error_message = str(e.mensaje)
            estatus = e.status
            response_error = {
            'status': estatus,
            'message': error_message
            }
            return Response(response_error,estatus)
        except Exception as e:
            return Response(f"Error {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get(self, request):
        try:
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
        except Exception as e:
            return Response(f"Error {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)