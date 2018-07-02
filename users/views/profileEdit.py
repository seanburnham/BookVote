from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from django.contrib.auth.decorators import login_required
from groups import models as gMod
from users import models as uMod
from django.http import HttpResponseRedirect
from formlib import Formless
from django import forms
import re
from django.contrib.auth import authenticate, login


@view_function
@login_required
def process_request(request):

    # process the form
    form = EditForm(request)
    if form.is_valid():
        form.commit()
        return HttpResponseRedirect('/users/profile')

    # render the template
    return request.dmp.render('profileEdit.html', {
        'form': form,
    })


class EditForm(Formless):
    def init(self):
        '''Adds the fields for this form'''
        self.fields['first_name'] = forms.CharField(label='First Name', initial = self.request.user.first_name)
        self.fields['last_name'] = forms.CharField(label='Last Name', initial = self.request.user.last_name)
        self.fields['username'] = forms.CharField(label='Username', initial = self.request.user.username, help_text = '* Usernames may only include alphanumeric characters, numbers, and spaces')
        self.fields['email'] = forms.EmailField(label='Email', initial = self.request.user.email, max_length=100, error_messages={'invalid': ("Email invalid.")})
        self.fields['oldPassword'] = forms.CharField(required=False, label='Old Password', widget=forms.PasswordInput(attrs={'placeholder': 'Old Password'}))
        self.fields['password'] = forms.CharField(required=False, label='New Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), help_text = '* Must contain at least 8 characters including a number')
        self.fields['password2'] = forms.CharField(required=False, label='Confirm New Password', widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
        self.fields['city'] = forms.CharField(required=False, label='City', initial = self.request.user.city)
        self.fields['state'] = forms.CharField(required=False, label='State', initial = self.request.user.state)
        self.fields['country'] = forms.CharField(required=False, label='Country', initial = self.request.user.country)
        self.fields['Goodreads'] = forms.CharField(required=False, label='Goodreads', initial = self.request.user.goodreadsAccount)
        self.fields['Facebook'] = forms.CharField(required=False, label='Facebook', initial = self.request.user.facebookAccount)
        self.fields['Google'] = forms.CharField(required=False, label='Google', initial = self.request.user.googleAccount)
        self.fields['Twitter'] = forms.CharField(required=False, label='Twitter', initial = self.request.user.twitterAccount)

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if username == self.request.user.username:
            return username

        if uMod.User.objects.filter(username=username).count() > 0:
            raise forms.ValidationError('This username is already taken. Please choose another.')

        chars = ('0123456789 abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        for char in username:
            if char not in chars:
                raise forms.ValidationError('Usernames may only inlcude alphanumeric characters, numbers, and spaces.')
            
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email == self.request.user.email:
            return email

        if uMod.User.objects.filter(email=email).count() > 0:
            raise forms.ValidationError('This email is already taken. Please use another.')
        return email

    def clean_oldPassword(self):
        op = self.cleaned_data.get('oldPassword')

        if op:
            if self.request.user.check_password(op):
                return op
            else:
                raise forms.ValidationError('Original password incorrect. Please try again.')
        else:
            return op

    def clean_password(self):
        pw1 = self.cleaned_data.get('password')
        op = self.cleaned_data.get('oldPassword')
        
        if not op and pw1:
             raise forms.ValidationError('Please make sure to enter original password.')

        if pw1:
            # check for special characters
            if not re.search('\d', pw1):
                raise forms.ValidationError('Please include at least one number.')
            # check for overall length
            if len(pw1) < 8:
                raise forms.ValidationError('Passwords must include at least 8 characters.')
        # return the value, per django spec
        return pw1

    def clean(self):
        pw1 = self.cleaned_data.get('password')
        pw2 = self.cleaned_data.get('password2')
        if pw1 and pw2:
            # ensure the passwords match
            if pw1 != pw2:
                raise forms.ValidationError('Please ensure the password fields match.')
            # return the cleaned data dict, per django spec
        return self.cleaned_data

    def commit(self):
        '''Process the form action'''
        u = self.request.user
        u.username = self.cleaned_data.get('username')
        u.email = self.cleaned_data.get('email')
        u.first_name = self.cleaned_data.get('first_name')
        u.last_name = self.cleaned_data.get('last_name')
        u.city = self.cleaned_data.get('city')
        u.state = self.cleaned_data.get('state')
        u.country = self.cleaned_data.get('country')
        u.goodreadsAccount = self.cleaned_data.get('Goodreads')
        u.facebookAccount = self.cleaned_data.get('Facebook')
        u.googleAccount = self.cleaned_data.get('Google')
        u.twitterAccount = self.cleaned_data.get('Twitter')
        u.save()

        if self.cleaned_data.get('oldPassword') and self.cleaned_data.get('password') and self.cleaned_data.get('password2'):
            u.set_password(self.cleaned_data.get('password'))
            u.save()
            login(self.request, u, backend='django.contrib.auth.backends.ModelBackend')