from django.db import models

class Books(models.Model):
	#ID
    title = models.TextField()
    author = models.TextField(null=True)
    isbn = models.TextField(null=True)
    image = models.TextField(null=True)
    users = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    avgRating = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    pageCount = models.IntegerField(null=True)
    upVotes = models.ManyToManyField('users.User', related_name='upVotes')
    downVotes = models.ManyToManyField('users.User', related_name='downVotes')
    description = models.TextField(null=True)
    dateCreated = models.DateTimeField(auto_now_add=True)