from django.contrib.auth.models import User, Group
from django.db import models

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_column="auth_user_id", related_name='detalles_usuario')
    image_profile = models.ImageField(upload_to='profiles/')
    image_cover = models.ImageField(upload_to='covers/')
    is_public = models.BooleanField(default=True)
   
    def __str__(self):
        return self.user.username

    class Meta:
        db_table = "Profile"