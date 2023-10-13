from django.contrib.auth.models import User, Group
from django.db import models

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, db_column='fk_user')
    images = models.ImageField(upload_to='posts/')
    descripcion = models.CharField(max_length=500, null = False)
    created_at = models.DateTimeField(auto_now_add=True)
   
    class Meta:
        db_table = "Post"