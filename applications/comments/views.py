from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from applications.comments.serializers import CommentSerializer,GetCommentsSerializer
from applications.profiles.models import Profile
from applications.posts.models import Post
from applications.followers.models import Follower
from applications.comments.models import Comment
from applications.history.models import History
from utils.exceptions import ExcepcionPersonalizada
from utils.responses import ResponseModel


class CommentList(APIView):
    
    def post(self,request):
        try:
            request.data['user'] = request.user.id
            post = Post.get_Post_byId(request.data['post'])
            if post == 0:
                raise ExcepcionPersonalizada('No se encontro el post', status=status.HTTP_204_NO_CONTENT)
            profile_who_post = Profile.get_profile(user = post.user)
            if profile_who_post == 0:
                raise ExcepcionPersonalizada('No se encontro el perfil que publico ese comentario', status=status.HTTP_204_NO_CONTENT)
            privacity = profile_who_post.is_public
            serializer=CommentSerializer(data=request.data)
            if serializer.is_valid():
                if request.user == profile_who_post.user or Follower.is_follower(request.user, profile_who_post.user):
                    serializer.save()
                    serializer_response = serializer.data
                    history_entry = History(username=request.user.username, event=f'Se ha creado un comentario en el post {post.id}')
                    history_entry.save()
                    response = ResponseModel.post_respond(serializer_response, True, title="creado el comentario")
                    return Response(response, status=status.HTTP_201_CREATED)
                if not privacity:
                        raise ExcepcionPersonalizada("Este perfil es privado, primero debes seguir a este usuario", status=status.HTTP_401_UNAUTHORIZED)
            raise ExcepcionPersonalizada(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
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
        
    
class ListCommentsByPost(APIView):
    def get(self, request, pk,):
        try:
            post = Post.get_Post_byId(pk)
            if post == 0:
                raise ExcepcionPersonalizada('No se encontro el elemento buscado', status=status.HTTP_204_NO_CONTENT)
            profile_who_post = Profile.get_profile(user = post.user)
            privacity = profile_who_post.is_public
            queryset = Comment.objects.filter(post = pk).order_by('id')
            serializer = GetCommentsSerializer(queryset, many=True, context={'request':request})
            if request.user == profile_who_post.user or Follower.is_follower(request.user, profile_who_post.user):
                response = ResponseModel.get_respond(success=True, data=serializer.data)
                return Response(response,status=200)
            if not privacity:  
                raise ExcepcionPersonalizada("Este perfil es privado, primero debes seguir a este usuario", status=status.HTTP_401_UNAUTHORIZED)
            response = ResponseModel.get_respond(success=True, data=serializer.data)
            return Response(response,status=200)
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
        
    