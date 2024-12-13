from django.db import models
from django.contrib.auth.models import User

class ImageRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    image_hash = models.CharField(max_length=64, unique=True)
    result = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
