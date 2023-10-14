from django.db import models
from django.contrib.auth.models import User

class Follower(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Follower"
        
    def is_follower(follower, profile_user):
        return Follower.objects.filter(follower=follower, followed=profile_user).exists()