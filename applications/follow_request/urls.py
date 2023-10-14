from django.urls import path
from applications.follow_request.views import ListFollowRequestView,FollowRequestDetailView

urlpatterns = [
    path('', ListFollowRequestView.as_view(), name='follow_requests'),
    path('<pk>/', FollowRequestDetailView.as_view(), name='follow_request_accepted'),
]