from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from applications.posts.serializers import PostSerializer,GetPostsSerializer
from applications.posts.models import Post
from applications.followers.models import Follower
from applications.profiles.models import Profile
from rest_framework.pagination import PageNumberPagination
from applications.history.models import History
from utils.exceptions import ExcepcionPersonalizada
from utils.responses import ResponseModel
from applications.comments.models import Comment
from applications.reactions.models import Reaction
from django.conf import settings


class PostList(APIView):

    def post(self,request):
        try:
            request.data['user'] = request.user.id
            serializer=PostSerializer(data=request.data)
            if serializer.is_valid():
                # asignar el usuario autenticado a la instancia de Post
                serializer.save()
                serializer_response = serializer.data
                history_entry = History(username=request.user.username, event=f'Realizo una publicacion')
                history_entry.save()
                response = ResponseModel.post_respond(serializer_response, True, title="creado la publicacion")
                return Response(response, status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(f"Error {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class UserPostsList(APIView):
    def get(self,request,pk):
        try:
            print(request.user)
            profile = Profile.get_profile(pk)
            if profile !=0:
                privacity = profile.is_public
                queryset = Post.objects.filter(user = pk).order_by('-created_at')
                serializer = GetPostsSerializer(queryset, many=True, context={'request':request})
                if request.user == profile.user or Follower.is_follower(request.user, profile.user):
                        response = ResponseModel.get_respond(success=True, data=serializer.data)
                        return Response(response, status=status.HTTP_200_OK)
                if not privacity:
                    raise ExcepcionPersonalizada("Este perfil es privado, primero debes seguir a este usuario", status=status.HTTP_401_UNAUTHORIZED)
                response = ResponseModel.get_respond(success=True, data=serializer.data)
                return Response(response, status=status.HTTP_200_OK)
            raise ExcepcionPersonalizada("No se encontro el perfil del usuario", status=status.HTTP_204_NO_CONTENT)
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
    
class PostByFollowedUsers(APIView):
    
    def get(self, request):
        try:
            user = request.user
            following_users = Follower.objects.filter(follower=user).values_list('followed', flat=True)
            following_profiles = Profile.objects.filter(user__in=following_users)
            queryset = Post.objects.filter(user__detalles_usuario__in=following_profiles).order_by('-created_at')

            # Paginación: crea una instancia de PageNumberPagination y obtén la página actual
            paginator = PageNumberPagination()
            result_page = paginator.paginate_queryset(queryset, request)
            
            # Modifica los resultados para asignar el username al campo user
            posts_with_username = [
                {
                    "id": post.id,
                    "images": post.images.url,
                    "descripcion": post.descripcion,
                    "created_at": post.created_at,
                    "comment_count": Comment.objects.filter(post=post).count(),
                    "reaction_count": Reaction.objects.filter(post=post).count(),
                    "view_comments": f"{settings.COMMENT_API_URL}{post.id}/",
                    "view_people_who_react": f"{settings.REACTION_API_URL}{post.id}/",
                }
                for post in result_page 
            ]

            # Devuelve la respuesta con el nuevo formato
            paginated_response = paginator.get_paginated_response(posts_with_username)
            return paginated_response
        except Exception as e:
            return Response(f"Error {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)