from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from applications.profiles.models import Profile
from django.core.files.storage import default_storage
from applications.posts.models import Post
from applications.posts.serializers import GetPostsSerializer
from django.conf import settings
from applications.followers.models import Follower
from applications.profiles.serializers import ChangeCoverPhotoSerializer, ChangeProfilePhotoSerializer, ChangPrivacySerializer,ViewProfileSerialier
from applications.history.models import History
from utils.exceptions import ExcepcionPersonalizada
from utils.responses import ResponseModel

class ChangeProfilePhotoView(APIView):

    def patch(self,request):
        try:
            profile = Profile.get_profile(request.user.id)
            
            if not profile:
                raise ExcepcionPersonalizada("No se encontro el perfil del usuario", status=status.HTTP_204_NO_CONTENT)                
            serializer = ChangeProfilePhotoSerializer(profile, data = request.data)
            if serializer.is_valid():
                image_url_original = profile.image_profile.url if profile.image_profile else None
                profile_updated = serializer.save()
                if image_url_original:
                    image_path_original = image_url_original.replace(settings.MEDIA_URL, '', 1)
                    default_storage.delete(image_path_original)
                print(profile_updated)
                data = {
                    "username": request.user.username,
                    "profile_photo": profile.image_profile.url if profile.image_profile else None
                }
                history_entry = History(username=request.user.username, event=f'Cambio su foto de perfil')
                history_entry.save()
                return Response(data, status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
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

class ChangeCoverPhotoView(APIView):
    def patch(self,request):
        profile = Profile.get_profile(request.user.id)
        
        if not profile:
            return Response("No se encontro el perfil del usuario", status=status.HTTP_204_NO_CONTENT)
            
        serializer = ChangeCoverPhotoSerializer(profile, data = request.data)
        if serializer.is_valid():
            image_url_original = profile.image_cover.url if profile.image_cover else None
            profile_updated = serializer.save()
            if image_url_original:
                image_path_original = image_url_original.replace(settings.MEDIA_URL, '', 1)
                default_storage.delete(image_path_original)
            print(profile_updated)
            data = {
                "username": request.user.username,
                "profile_photo": profile.image_cover.url if profile.image_cover else None
            }
            history_entry = History(username=request.user.username, event=f'Cambio su foto de portada')
            history_entry.save()
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class ChangePrivacityView(APIView):
    def patch(self, request):
        profile = Profile.get_profile(request.user.id)
        

        if not profile:
            return Response("No se encontro el perfil del usuario", status=status.HTTP_204_NO_CONTENT)
        
        serializer = ChangPrivacySerializer(profile, data = request.data)
        if serializer.is_valid():
            serializer.save()
            datas = serializer.data
            history_entry = History(username=request.user.username, event=f'Cambio la privacidad de su perfil')
            history_entry.save()
            return Response(datas, status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ViewProflieView(APIView):
    
    def get(self, request,pk):
        profile = Profile.get_profile(pk)
        # Si encuenttra el id de la membresia, lo manda como response
        if profile != 0:
            posts = Post.objects.filter(user=profile.user)
            serializer = ViewProfileSerialier(profile)
            serialized_data = serializer.data
            serialized_data['posts'] = GetPostsSerializer(posts, many=True).data
            privacity = serializer.data['is_public']
            if request.user == profile.user or Follower.is_follower(request.user, profile.user):
                return Response(serialized_data, status=status.HTTP_200_OK)
            
            if not privacity:
                return Response("Este perfil es privado, primero debes seguir a este usuario", status=status.HTTP_204_NO_CONTENT)
            
            return Response(serialized_data, status=status.HTTP_200_OK)
        return Response("No se encontro el perfil del usuario", status=status.HTTP_204_NO_CONTENT)
