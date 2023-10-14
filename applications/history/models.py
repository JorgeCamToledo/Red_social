from djongo import models

# Create your models here.
class History(models.Model):
    username = models.CharField(max_length=500)
    event = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "History"
