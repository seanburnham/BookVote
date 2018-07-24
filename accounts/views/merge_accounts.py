from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from django.contrib.auth.decorators import login_required
from users import models as uMod
import requests
import json
from formlib import Formless
from django import forms
from social_django.models import UserSocialAuth

@view_function
# @login_required
def process_request(request, userID, socialID):
    
    user = uMod.User.objects.get(id=userID)

    form = MergeForm(request)
    if form.is_valid():

        junk = uMod.Junk.objects.get(identifier = socialID)

        social_user = UserSocialAuth() 
        social_user.provider = junk.data1
        social_user.uid = junk.data2
        social_user.extra_data = json.loads(junk.data3)
        social_user.user_id = user.id
        social_user.save()

        junk.delete()

        form.commit()
        return HttpResponseRedirect('/homepage/index/')
        
    context = {
        'user': user,
        'form': form,
    }

    return request.dmp.render('merge_accounts.html', context)

class MergeForm(Formless):
    def init(self):
        '''Adds the fields for this form'''
        self.fields['username'] = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Username or Email'}))
        self.fields['password'] = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': '******'}))
        self.user = None

    def clean(self):
        self.user = authenticate(username=self.cleaned_data.get('username'), password=self.cleaned_data.get('password'))
        if self.user is None:
            raise forms.ValidationError('Invalid email or password.')
        # return the cleaned data dict, per django spec
        return self.cleaned_data

    def commit(self):
        '''Process the form action'''
        login(self.request, self.user)