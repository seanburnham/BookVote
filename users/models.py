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
    emailNotifications = models.BooleanField(default=True)

class ResetPasswordTokens(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    token = models.TextField()
    dateCreated = models.DateTimeField(auto_now_add=True)

class Junk(models.Model):
    # identifier for unique row (id of some sort)
	identifier = models.TextField(null=True)
	data1 = models.TextField(null=True)
	data2 = models.TextField(null=True)
	data3 = models.TextField(null=True)
	data4 = models.TextField(null=True)
	data5 = models.TextField(null=True)
	data6 = models.TextField(null=True)
