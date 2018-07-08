from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from formlib import Formless
from django import forms
import requests
import json

@view_function
def process_request(request):

    # process the form
    form = LoginForm(request)
    form.submit_text = 'Login'
    if form.is_valid():
        form.commit()
        return HttpResponseRedirect('/')

    # render the template
    return request.dmp.render('login.html', {
        'form': form,
    })


class LoginForm(Formless):
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