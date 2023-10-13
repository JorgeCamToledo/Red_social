from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from applications.posts.serializers import PostSerializer


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