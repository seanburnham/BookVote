from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from django.contrib.auth.decorators import login_required
from books import models as bMod
from django.db.models import Count

@view_function
@login_required
def process_request(request):

    try:
        bookList = bMod.Books.objects.annotate(q_count=Count('upVotes')).order_by('-q_count','dateCreated')
    except:
        bookList = []

    context = {
        'bookList': bookList,
    }
    return request.dmp.render('rankings.html', context)