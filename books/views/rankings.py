from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from django.contrib.auth.decorators import login_required
from books import models as bMod
from groups import models as gMod
from users import models as uMod
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.core.mail import send_mail, send_mass_mail

@view_function
@login_required
def process_request(request):

    groups = gMod.Group.objects.filter(users__id__contains = request.user.id)

    bookDict = {}


    for g in groups:
        bookDict[g] = g.bookList.all().annotate(q_count=Count('upVotes')).order_by('-q_count', '-avgRating', 'dateCreated')


    if request.method == "POST":
        try:
            group = gMod.Group.objects.get(id = request.POST.get('group'))
            if group.currentBook != None:
                group.readBookList.add(bMod.Books.objects.get(id=group.currentBook.id))
            
            group.bookList.remove(bMod.Books.objects.get(id=request.POST.get('book')))
            group.currentBookDeadline = request.POST.get('deadline')
            group.currentBook = bMod.Books.objects.get(id=request.POST.get('book'))
            group.save()

            subject = 'New Book to Read for ' + group.name
            message = group.currentBook.title + ' has been selected as the new book to read as a group. The deadline for this book has been set to ' + group.currentBookDeadline
            email_from = settings.EMAIL_HOST_USER
            # recipient_list = ['seanburnham92@yahoo.com',]

            datatuple = ()

            for u in group.users.all():
                datatuple += (subject, message, email_from, [u.email])

            print('-=--=-=-=-=-=-=-=-=-=-=',datatuple)

            send_mass_mail(datatuple)
            # send_mail( subject, message, email_from, recipient_list )

            # return HttpResponseRedirect('/books/bookvote/' + request.POST.get('group'))

        except:
            pass


    context = {
        'bookDict': bookDict,
    }
    return request.dmp.render('rankings.html', context)
