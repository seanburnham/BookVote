from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    city = models.TextField(null=True)
    state = models.TextField(null=True)
    country = models.TextField(null=True)
    activatedAccount = models.BooleanField(default=False)
    dateCreated = models.DateTimeField(auto_now_add=True, null=True)
    last_active = models.DateTimeField(null=True)
    goodreadsAccount = models.TextField(null=True)
    facebookAccount = models.TextField(null=True)
    googleAccount = models.TextField(null=True)
    twitterAccount = models.TextField(null=True)

class ResetPasswordTokens(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    token = models.TextField()
    dateCreated = models.DateTimeField(auto_now_add=True)