from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from django.contrib.auth.decorators import login_required
from groups import models as gMod

@view_function
@login_required
def process_request(request):
    
    try:
        userGroups = gMod.Group.objects.filter(users__id__contains = request.user.id)
    except:
        userGroups = []

    groups = gMod.Group.objects.exclude(users__id__contains = request.user.id)

    context = {
        'userGroups': userGroups,
        'groups':groups,
    }
    return request.dmp.render('index.html', context)

@view_function
@login_required
def addGroup(request, groupID):

    try:
        group = gMod.Group.objects.get(id = groupID)
        if group.is_private:
            if request.user in group.pendingApprovals.all():
                pass
            else:
                group.pendingApprovals.add(request.user)
        else:
            group.users.add(request.user)
    except:
        pass

    try:
        userGroups = gMod.Group.objects.filter(users__id__contains = request.user.id)
    except:
        userGroups = []

    context = {
        'userGroups': userGroups,
    }
    return request.dmp.render('index.addGroup.html', context)
