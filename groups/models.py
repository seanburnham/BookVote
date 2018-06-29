from django.db import models

# Create your models here.
class Group(models.Model):
    name = models.TextField(null=False)
    description = models.TextField(null=True)
    users = models.ManyToManyField('users.User', related_name='users')
    bookList = models.ManyToManyField('books.Books', related_name='bookList')
    readBookList = models.ManyToManyField('books.Books', related_name='readBookList')
    is_private = models.BooleanField(default=False)
    pendingApprovals = models.ManyToManyField('users.User', related_name='pendingApprovals')
    admin_users = models.ManyToManyField('users.User', related_name='admin_users')
    currentBook = models.ForeignKey('books.Books', on_delete=models.SET_NULL, null=True, related_name='currentBook')
    currentBookDeadline = models.DateField(null=True)
    dateCreated = models.DateTimeField(auto_now_add=True)