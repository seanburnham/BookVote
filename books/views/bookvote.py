from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone

import json
from django.http import HttpResponse
import sys

from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from books import models as bMod
from django.contrib.auth.decorators import login_required
import requests
import xmltodict


@view_function
@login_required
def process_request(request):


    try:
        bookList = bMod.Books.objects.exclude(upVotes__id__contains =request.user.id).exclude(downVotes__id__contains =request.user.id).order_by('-dateCreated');
    except:
        bookList = []


    # if request.method == "POST":
    #     try:
    #         b = bMod.Books.objects.get(isbn = request.POST.get('isbn'))
    #     except:
    #         key = "Te7ahdToiP8n7iV3Lpgw6g"

    #         #Grab data from Goodreads API
    #         response = requests.get("https://www.goodreads.com/search.xml?key=" + key + "&q=" + request.POST.get('isbn'))
    #         o = xmltodict.parse(response.content)
    #         result_tree = json.loads(json.dumps(o))
            
    #         print(result_tree['GoodreadsResponse']['search']['results']['work']['average_rating'])
                

    #         b = bMod.Books()
    #         b.title = request.POST.get('title')
    #         b.author = request.POST.get('author')
    #         b.isbn = request.POST.get('isbn')
    #         b.image = request.POST.get('image')
    #         b.description = request.POST.get('description')
    #         b.avgRating = result_tree['GoodreadsResponse']['search']['results']['work']['average_rating']
    #         b.pageCount = request.POST.get('pageCount')
    #         b.users_id = request.user.id
    #         b.save()

    
    # csrfContext = RequestContext(request)

    # print('-=-=-=-=-=-=-=-=-=-', bookList)

    context = {
        'bookList': bookList,
    }

    return request.dmp.render('bookvote.html', context)


@view_function
@login_required
def addToList(request, isbn):
    # add upVote to database
    
    try:
        book = bMod.Books.objects.get(isbn = isbn)
    except:
        #Grab data from Goodreads API
        goodReadsKey = "Te7ahdToiP8n7iV3Lpgw6g"
        response = requests.get("https://www.goodreads.com/search.xml?key=" + goodReadsKey + "&q=" + isbn)
        o = xmltodict.parse(response.content)
        goodreads_tree = json.loads(json.dumps(o))

        #Grab data from Google API
        googleKey = "AIzaSyDNoBh8E3DyB1PTktxBE2ZLpIK2kIPipS4"
        response2 = requests.get("https://www.googleapis.com/books/v1/volumes?q=" + isbn + "&key=" + googleKey)
        google_tree = json.loads(response2.content)

        #Create a new book
        b = bMod.Books()
        b.title = goodreads_tree['GoodreadsResponse']['search']['results']['work']['best_book']['title']
        b.author = goodreads_tree['GoodreadsResponse']['search']['results']['work']['best_book']['author']['name']
        b.isbn = isbn
        b.image = google_tree['items'][0]['volumeInfo']['imageLinks']['smallThumbnail']
        b.description = google_tree['items'][0]['volumeInfo']['description']
        b.avgRating = goodreads_tree['GoodreadsResponse']['search']['results']['work']['average_rating']
        b.pageCount = google_tree['items'][0]['volumeInfo']['pageCount']
        b.users_id = request.user.id
        b.save()

    try:
        bookList = bMod.Books.objects.exclude(upVotes__id__contains = request.user.id).exclude(downVotes__id__contains = request.user.id).order_by('-dateCreated');
    except:
        bookList = []

    context = {
        'bookList': bookList,
    }
    return request.dmp.render('bookvote.vote.html', context)



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
