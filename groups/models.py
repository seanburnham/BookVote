from django.db import models

# Create your models here.
class Group(models.Model):
    name = models.TextField(null=False)
    description = models.TextField(null=True)
    users = models.ManyToManyField('users.User', related_name='users')
    bookList = models.ManyToManyField('books.Books', related_name='bookList')
    is_private = models.BooleanField(default=False)
    passphrase = models.TextField(null=True)
    admin_users = models.ManyToManyField('users.User', related_name='admin_users')
    currentBook = models.ForeignKey('books.Books', on_delete=models.SET_NULL, null=True, related_name='currentBook')
    dateCreated = models.DateTimeField(auto_now_add=True)