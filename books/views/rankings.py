from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from django.contrib.auth.decorators import login_required
from books import models as bMod

@view_function
@login_required
def process_request(request):

    try:
        bookList = bMod.Books.objects.order_by('-dateCreated').order_by('upVotes')
    except:
        bookList = []

    print('-=-=-=-=-=-=-=-=-=-=-=-=-=',bookList)

    context = {
        'bookList': bookList,
    }
    return request.dmp.render('rankings.html', context)