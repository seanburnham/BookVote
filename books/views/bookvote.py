from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone

import json
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import sys

from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from books import models as bMod
from groups import models as gMod
from users import models as uMod
from django.contrib.auth.decorators import login_required
import requests
import xmltodict
import re


@view_function
@login_required
def process_request(request, groupID):

    group = gMod.Group.objects.get(id = int(groupID))

    if request.user in group.users.all():
        try:
            books = group.bookList.all()
            bookList = bMod.Books.objects.filter(id__in = books).exclude(upVotes__id__contains =request.user.id).exclude(downVotes__id__contains =request.user.id).order_by('-dateCreated')
        except:
            bookList = []

        try:
            currentBook = bMod.Books.objects.get(id=group.currentBook.id)
        except:
            currentBook = None


        context = {
            'bookList': bookList,
            'group': group,
            'currentBook': currentBook,
        }

        return request.dmp.render('bookvote.html', context)
    else:
        return HttpResponseRedirect('/')


@view_function
@login_required
def addToList(request, groupID, bookID):
    # add upVote to database
    

    try:
        book = bMod.Books.objects.get(bookID = bookID)

        group = gMod.Group.objects.get(id=groupID)
        group.bookList.add(book)    
    
    except:
        # "9781683690405"
        #Grab data from Goodreads API
        # goodReadsKey = "Te7ahdToiP8n7iV3Lpgw6g"
        # response = requests.get("https://www.goodreads.com/search.xml?key=" + goodReadsKey + "&q=" + isbn)
        # o = xmltodict.parse(response.content)
        # goodreads_tree = json.loads(json.dumps(o))

        # title = goodreads_tree['GoodreadsResponse']['search']['results']['work']['best_book']['title']

        # https://www.goodreads.com/book/show/17340050.xml?key=Te7ahdToiP8n7iV3Lpgw6g
        goodReadsKey = "Te7ahdToiP8n7iV3Lpgw6g"
        # response = requests.get("https://www.goodreads.com/search.xml?key=" + goodReadsKey + "&q=" + bookID)
        response = requests.get("https://www.goodreads.com/book/show/" + bookID + ".xml?key=" + goodReadsKey)
        o = xmltodict.parse(response.content)
        goodreads_tree = json.loads(json.dumps(o))

        # desc = goodreads_tree['GoodreadsResponse']['book']['description']
        # print(goodreads_tree)
        # print(len(goodreads_tree['GoodreadsResponse']['book']['authors']['author'][0]), '-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
        # print('+++++++++++++++++++++',goodreads_tree['GoodreadsResponse']['book']['authors']['author']['name'])

        def cleanhtml(raw_html):
            cleanr = re.compile('<.*?>')
            cleantext = re.sub(cleanr, '', raw_html)
            return cleantext

        # print(cleanhtml(desc))

        # #Grab data from Google API
        # #Search by goodreads title data because google results end up grabbing multiple books even under one isbn
        # googleKey = "AIzaSyDNoBh8E3DyB1PTktxBE2ZLpIK2kIPipS4"
        # response2 = requests.get("https://www.googleapis.com/books/v1/volumes?q=" + title + "&key=" + googleKey)
        # google_tree = json.loads(response2.content)

        #Create a new book
        b = bMod.Books()
        b.title = goodreads_tree['GoodreadsResponse']['book']['title']
        try: 
            b.author = goodreads_tree['GoodreadsResponse']['book']['authors']['author'][0]['name']
        except:
            b.author = goodreads_tree['GoodreadsResponse']['book']['authors']['author']['name']
        b.bookID = bookID
        b.image = goodreads_tree['GoodreadsResponse']['book']['small_image_url']
        b.description = cleanhtml(goodreads_tree['GoodreadsResponse']['book']['description'])
        b.avgRating = goodreads_tree['GoodreadsResponse']['book']['average_rating']
        b.pageCount = goodreads_tree['GoodreadsResponse']['book']['num_pages']
        b.users_id = request.user.id
        b.save()

        #Add to current group
        group = gMod.Group.objects.get(id=groupID)
        group.bookList.add(b)

    try:
        books = group.bookList.all()
        bookList = bMod.Books.objects.filter(id__in = books).exclude(upVotes__id__contains =request.user.id).exclude(downVotes__id__contains =request.user.id).order_by('-dateCreated');
    except:
        bookList = []

    context = {
        'bookList': bookList,
    }
    return request.dmp.render('bookvote.vote.html', context)



@view_function
@login_required
def upVote(request, groupID, bookID):
    # add upVote to database
    
    try:
        book = bMod.Books.objects.get(id = bookID)
        book.upVotes.add(request.user)
    except:
        pass

    group = gMod.Group.objects.get(id=groupID)

    try:
        books = group.bookList.all()
        bookList = bMod.Books.objects.filter(id__in = books).exclude(upVotes__id__contains =request.user.id).exclude(downVotes__id__contains =request.user.id).order_by('-dateCreated');
    except:
        bookList = []

    context = {
        'bookList': bookList,
    }
    return request.dmp.render('bookvote.vote.html', context)

@view_function
@login_required
def downVote(request, groupID, bookID):
    # add downVote to database
    
    try:
        book = bMod.Books.objects.get(id = bookID)
        book.downVotes.add(request.user)
    except:
        pass

    group = gMod.Group.objects.get(id=groupID)

    try:
        books = group.bookList.all()
        bookList = bMod.Books.objects.filter(id__in = books).exclude(upVotes__id__contains =request.user.id).exclude(downVotes__id__contains =request.user.id).order_by('-dateCreated');
    except:
        bookList = []

    context = {
        'bookList': bookList,
    }
    return request.dmp.render('bookvote.vote.html', context)

@view_function
@login_required
def removeGroupMember(request, groupID, userID):

    group = gMod.Group.objects.get(id = groupID)
    user = uMod.User.objects.get(id=userID)

    if request.user in group.admin_users.all():
        group.users.remove(user)
        if user in group.admin_users.all():
            group.admin_users.remove(user)


    context = {
        'group':group,
    }
    return request.dmp.render('bookvote.removeGroupMember.html', context)


@view_function
@login_required
def pendingApproval(request, groupID, userID, approvalStatus):

    group = gMod.Group.objects.get(id = groupID)
    user = uMod.User.objects.get(id=userID)

    if request.user in group.admin_users.all():
        if approvalStatus == 'accept':
            group.users.add(user)
            group.pendingApprovals.remove(user)
        elif approvalStatus == 'reject':
            group.pendingApprovals.remove(user)
        else:
            pass


    context = {
        'group':group,
    }
    return request.dmp.render('bookvote.pendingApproval.html', context)

    
@view_function
@login_required
def addAdminUser(request, groupID, userID):

    group = gMod.Group.objects.get(id = groupID)
    user = uMod.User.objects.get(id=userID)

    if request.user in group.admin_users.all():
        if user not in group.admin_users.all():
            group.admin_users.add(user)
        else:
            pass


    context = {
        'group':group,
    }
    return request.dmp.render('bookvote.pendingApproval.html', context)

    