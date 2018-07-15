from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from django.contrib.auth.decorators import login_required
from groups import models as gMod
from users import models as uMod
from django.http import HttpResponse, HttpResponseRedirect


@view_function
@login_required
def process_request(request):
    return request.dmp.render('profile.html')


@view_function
@login_required
def leaveGroup(request, groupID):
    # add upVote to database
    
    try:
        group = gMod.Group.objects.get(id=groupID)
        group.users.remove(request.user)
        if request.user in group.admin_users.all():
            group.admin_users.remove(request.user)
    except:
        pass

    return request.dmp.render('profile.leaveGroup.html')


@view_function
@login_required
def update_settings(request):

    u = uMod.User.objects.get(id=request.user.id)

    if request.POST.get('settings') == '1':
        u.emailNotifications = True
        u.save()
    else:
        u.emailNotifications = False
        u.save()


    return HttpResponse("Success")