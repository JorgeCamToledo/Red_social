from django.contrib.auth.models import User
from django.db import models
from applications.posts.models import Post

# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='fk_user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, db_column='fk_post')
    text = models.CharField(max_length=500, null = False)
    timestap = models.DateTimeField(auto_now_add=True)  

    class Meta:
        db_table = "Comments"