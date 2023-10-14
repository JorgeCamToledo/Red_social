from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from applications.followers.models import Follower
from applications.follow_request.models import FollowRequest
from applications.follow_request.serializers import GetFollowRequestSerializer
from applications.history.models import History
class ListFollowRequestView(APIView):
    
    def get(self,request):
        user = request.user.id
        follow_requests = FollowRequest.objects.filter(receiver = user)
        serializer = GetFollowRequestSerializer(follow_requests,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class FollowRequestDetailView(APIView):
    def put(self, request, pk):
        follow_request = FollowRequest.get_followRequest(pk)
        
        if follow_request != 0:
            if request.user != follow_request.receiver:
                return Response("No tienes permiso para aprobar esta solicitud.", status=status.HTTP_403_FORBIDDEN)

            follow_request.approved = True
            requester = follow_request.requester
            print(requester)
            follow_request.save()
            follower, created = Follower.objects.get_or_create(follower=follow_request.requester, followed=request.user)
            history_entry = History(username=request.user.username, event=f'acepto la solicitud de {requester}')
            history_entry.save()
            return Response(f"Solicitud de {requester} aprobada", status=status.HTTP_200_OK)
        return Response("No se encontro el elemento buscado", status=status.HTTP_204_NO_CONTENT)
        
        