from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from applications.followers.models import Follower
from applications.follow_request.models import FollowRequest
from applications.follow_request.serializers import GetFollowRequestSerializer
from applications.history.models import History
from utils.responses import ResponseModel
from utils.exceptions import ExcepcionPersonalizada
class ListFollowRequestView(APIView):
    
    def get(self,request):
        try:
            user = request.user.id
            follow_requests = FollowRequest.objects.filter(receiver = user)
            serializer = GetFollowRequestSerializer(follow_requests,many=True)
            response = ResponseModel.get_respond(success=True, data=serializer.data)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f"Error {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class FollowRequestDetailView(APIView):
    def put(self, request, pk):
        try:
            follow_request = FollowRequest.get_followRequest(pk)
            if follow_request != 0:
                if request.user != follow_request.receiver:
                    raise ExcepcionPersonalizada("No tienes permiso para aprobar esta solicitud.", status=status.HTTP_403_FORBIDDEN)
                follow_request.approved = True
                requester = follow_request.requester
                print(requester)
                follow_request.save()
                follower, created = Follower.objects.get_or_create(follower=follow_request.requester, followed=request.user)
                history_entry = History(username=request.user.username, event=f'acepto la solicitud de {requester}')
                history_entry.save()
                return Response({"message":f"Solicitud de {requester} aprobada"}, status=status.HTTP_200_OK)
            raise ExcepcionPersonalizada("No se encontro el elemento buscado", status=status.HTTP_204_NO_CONTENT)
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
        
        