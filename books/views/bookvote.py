from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone

import json
from django.http import HttpResponse
# import requests
import sys

from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from books import models as bMod
from django.contrib.auth.decorators import login_required

@view_function
@login_required
def process_request(request):
    
    try:
        bookList = bMod.Books.objects.exclude(upVotes__id__contains =request.user.id).exclude(downVotes__id__contains =request.user.id).order_by('-dateCreated');
    except:
        bookList = []

    if request.method == "POST":
        try:
            b = bMod.Books.objects.get(isbn = request.POST.get('isbn'))
        except:
            b = bMod.Books()
            b.title = request.POST.get('title')
            b.author = request.POST.get('author')
            b.isbn = request.POST.get('isbn')
            b.image = request.POST.get('image')
            b.description = request.POST.get('description')
            b.avgRating = request.POST.get('avgRating')
            b.pageCount = request.POST.get('pageCount')
            b.users_id = request.user.id
            b.save()

    
    # csrfContext = RequestContext(request)

    # print('-=-=-=-=-=-=-=-=-=-', bookList)

    context = {
        'bookList': bookList,
    }

    return request.dmp.render('bookvote.html', context)



@view_function
@login_required
def upVote(request, bookID):
    # add upVote to database
    
    try:
        book = bMod.Books.objects.get(id = bookID)
        book.upVotes.add(request.user)
    except:
        pass

    try:
        bookList = bMod.Books.objects.exclude(upVotes__id__contains =request.user.id).exclude(downVotes__id__contains =request.user.id).order_by('-dateCreated');
    except:
        bookList = []

    context = {
        'bookList': bookList,
    }
    return request.dmp.render('bookvote.vote.html', context)

@view_function
@login_required
def downVote(request, bookID):
    # add upVote to database
    
    try:
        book = bMod.Books.objects.get(id = bookID)
        book.downVotes.add(request.user)
    except:
        pass

    try:
        bookList = bMod.Books.objects.exclude(upVotes__id__contains =request.user.id).exclude(downVotes__id__contains =request.user.id).order_by('-dateCreated');
    except:
        bookList = []

    context = {
        'bookList': bookList,
    }
    return request.dmp.render('bookvote.vote.html', context)
