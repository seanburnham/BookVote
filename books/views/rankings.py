from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from django.contrib.auth.decorators import login_required
from books import models as bMod
from groups import models as gMod
from django.db.models import Count

@view_function
@login_required
def process_request(request):

    groups = gMod.Group.objects.filter(users__id__contains = request.user.id)

    bookDict = {}


    for g in groups:
        bookDict[g.name] = g.bookList.all().annotate(q_count=Count('upVotes')).order_by('-q_count', '-avgRating', 'dateCreated')

    # try:
    #     bookList = bMod.Books.objects.annotate(q_count=Count('upVotes')).order_by('-q_count', '-avgRating', 'dateCreated')
    # except:
    #     bookList = []

    context = {
        'bookDict': bookDict,
    }
    return request.dmp.render('rankings.html', context)