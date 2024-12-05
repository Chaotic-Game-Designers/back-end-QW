from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class DeviceToken(models.Model):
    token = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
