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
from django.core.mail import send_mail, send_mass_mail, EmailMultiAlternatives, get_connection

@view_function
@login_required
def process_request(request):

    groups = gMod.Group.objects.filter(users__id__contains = request.user.id)

    bookDict = {}


    for g in groups:
        bookDict[g] = g.bookList.all().annotate(q_count=Count('upVotes')).order_by('-q_count', '-avgRating', 'dateCreated')


    if request.method == "POST":
        # try:
        group = gMod.Group.objects.get(id = request.POST.get('group'))
        if group.currentBook != None:
            group.readBookList.add(bMod.Books.objects.get(id=group.currentBook.id))
        
        group.bookList.remove(bMod.Books.objects.get(id=request.POST.get('book')))
        group.currentBookDeadline = request.POST.get('deadline')
        group.currentBook = bMod.Books.objects.get(id=request.POST.get('book'))
        group.save()


        connection = get_connection() # uses SMTP server specified in settings.py
        connection.open() # If you don't open the connection manually, Django will automatically open, then tear down the connection in msg.send()
        messages = []
        subject = 'New Book to Read for ' + group.name
        text_content = '...'
        html_content = '<p><a href="https://www.goodreads.com/book/isbn/' + group.currentBook.isbn + '">' + group.currentBook.title + '</a> by ' + group.currentBook.author + ' has been selected as the new book to read as a group.</p>' + '\n\n'  + '<p>The deadline for this book has been set to ' + str(group.currentBookDeadline) + '</p>'  

        for u in group.users.all():
            message = EmailMultiAlternatives(subject, text_content,  settings.EMAIL_HOST_USER, [u.email,])
            message.attach_alternative(html_content, 'text/html')
            messages.append(message)  
        
        connection.send_messages(messages)

        connection.close() # Cleanup


            # subject = 'New Book to Read for ' + group.name
            # message = group.currentBook.title + ' by ' + group.currentBook.author + ' has been selected as the new book to read as a group.\n\n The deadline for this book has been set to ' + str(group.currentBookDeadline)
            # email_from = settings.EMAIL_HOST_USER
            # # recipient_list = ['sburnham92@gmail.com',]

            # datatuple = ()

            # for u in group.users.all():
            #     datatuple = datatuple + ((subject, message, email_from, [u.email]),)

            # # print('-=--=-=-=-=-=-=-=-=-=-=',datatuple)

            # send_mass_mail(datatuple)
            
            # send_mail( subject, message, email_from, recipient_list )
            # send_mail('Hello', "Here is your password reset token:\n\n" + base_url + "accounts/forgot_password_token/" + generateToken() + "\n\nKeep on Reading!", 'bookvotingapp@gmail.com', [email])


            # return HttpResponseRedirect('/books/bookvote/' + request.POST.get('group'))

        # except:
        #     pass


    context = {
        'bookDict': bookDict,
    }
    return request.dmp.render('rankings.html', context)
