from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from django.contrib.auth.decorators import login_required
from users import models as uMod
import requests
import json


@view_function
def process_request(request):
    if request.user:
        social_user = request.user.social_auth.filter(provider='facebook',).first()

        if social_user: 
            url = 'https://graph.facebook.com/{0}?fields=id,name,email&access_token={1}'.format(
                social_user.uid,
                social_user.extra_data['access_token'],
                )

            response = requests.get(url)
            o = json.loads(response.content)

            facebookUser = uMod.User.objects.get(id=request.user.id)

            userList = uMod.User.objects.filter(email=o['email'])
            print('-=-=-=-=-=-=-', userList)
            if userList.count() > 1:

                if userList[0].id < userList[1].id:
                    userID = userList[0].id
                else:
                    userID = userList[1].id

                try:
                    junk = uMod.Junk.objects.get(identifier=social_user.id)
                    junk.delete()
                except:
                    pass
                
                junk = uMod.Junk()
                junk.identifier = social_user.id
                junk.data1 = social_user.provider 
                junk.data2 = social_user.uid
                junk.data3 = json.dumps(social_user.extra_data)
                junk.data4 = social_user.user_id
                junk.save()

                socialAccountID = social_user.id

                facebookUser.delete()

                return HttpResponseRedirect('/accounts/merge_accounts/' + str(userID) + '/' + str(socialAccountID) + '/')
            else:
                pass

    return HttpResponseRedirect('/homepage/index/')