from django.db import models
from django.contrib.auth.models import User

class FollowRequest(models.Model):
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follow_requests_sent')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follow_requests_received')
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    
    class Meta:
        db_table = "Follower_request"
    
    def get_followRequest(pk):
        try:
            return FollowRequest.objects.get(id=pk)
        except FollowRequest.DoesNotExist:
            return 0