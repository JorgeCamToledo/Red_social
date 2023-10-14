from applications.reactions.views import ReactionList, ListReactionsByPost
from django.urls import path

urlpatterns = [
    path('', ReactionList.as_view(), name='comentar'),   
    path('by_post/<pk>/', ListReactionsByPost.as_view(), name='ver_reacciones'),       
]