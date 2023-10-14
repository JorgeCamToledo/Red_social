from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from applications.profiles.models import Profile
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from applications.followers.models import Follower
from applications.profiles.serializers import ChangeCoverPhotoSerializer, ChangeProfilePhotoSerializer, ChangPrivacySerializer,ViewProfileSerialier


class ChangeProfilePhotoView(APIView):

    def patch(self,request):
        profile = Profile.get_profile(request.user.id)
        
        if not profile:
            return Response("No se encontro el perfil del usuario", status=status.HTTP_204_NO_CONTENT)
            
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
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

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
            return Response(datas, status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ViewProflieView(APIView):
    
    def get(self, request,pk):
        profile = Profile.get_profile(pk)
        # Si encuenttra el id de la membresia, lo manda como response
        if profile != 0:
            serializer = ViewProfileSerialier(profile)
            privacity = serializer.data['is_public']
            if request.user == profile.user or Follower.is_follower(request.user, profile.user):
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            if not privacity:
                return Response("Este perfil es privado, primero debes seguir a este usuario", status=status.HTTP_204_NO_CONTENT)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response("No se encontro el perfil del usuario", status=status.HTTP_204_NO_CONTENT)
