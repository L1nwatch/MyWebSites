from django.db import models
from django.utils import timezone


# Create your models here.
class User(models.Model):
    email = models.EmailField()
    last_login = models.DateTimeField(default=timezone.now)
    REQUIRED_FIELDS = ()
    USERNAME_FIELD = "email"
