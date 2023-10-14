from applications.comments.views import CommentList,ListCommentsByPost
from django.urls import path

urlpatterns = [
    path('', CommentList.as_view(), name='comentar'),   
    path('by_post/<pk>/', ListCommentsByPost.as_view(), name='ver_comentarios_deUn_Post'),    
]