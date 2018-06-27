from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from django.contrib.auth.decorators import login_required
from books import models as bMod
from groups import models as gMod
from users import models as uMod
from django.db.models import Count

@view_function
@login_required
def process_request(request):

    groups = gMod.Group.objects.filter(users__id__contains = request.user.id)

    bookDict = {}

    users = uMod.User.objects.all()
    group1 = gMod.Group.objects.get(id=1)
    books = bMod.Books.objects.all()

    for u in users:
        group1.users.add(u)

    for b in books:
        group1.bookList.add(b)


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