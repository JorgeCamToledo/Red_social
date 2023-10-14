from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from applications.followers.models import Follower
from applications.profiles.models import Profile
from applications.follow_request.models import FollowRequest
from applications.follow_request.serializers import FollowRequestSerializer

class ListFollowRequestView(APIView):
    
    def get(self,request):
        user = request.user.id
        follow_requests = FollowRequest.objects.filter(receiver = user)
        serializer = FollowRequestSerializer(follow_requests,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class FollowRequestDetailView(APIView):
    def put(self, request, pk):
        follow_request = FollowRequest.objects.get(id=pk)

        if request.user != follow_request.receiver:
            return Response("No tienes permiso para aprobar esta solicitud.", status=status.HTTP_403_FORBIDDEN)

        follow_request.approved = True
        follow_request.save()
        follower, created = Follower.objects.get_or_create(follower=follow_request.requester, followed=request.user)
        return Response("Solicitud aprobada.", status=status.HTTP_200_OK)
        
        