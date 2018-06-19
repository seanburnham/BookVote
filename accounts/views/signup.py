from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from formlib import Formless
from django import forms
from users import models as umod
import re

@view_function
def process_request(request):
    # process the form
    form = Signup(request)
    if form.is_valid():
        form.commit()
        return HttpResponseRedirect('/')

    # render the template
    return request.dmp.render('signup.html', {
        'form': form,
    })


class Signup(Formless):
    def init(self):

        '''Adds the fields for this form'''
        self.fields['first_name'] = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
        self.fields['last_name'] = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
        self.fields['username'] = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Username'}), help_text = '* Usernames may only inlcude alphanumeric characters, numbers, and spaces')
        self.fields['email'] = forms.EmailField(label="",widget=forms.EmailInput(attrs={'placeholder': 'Email','class':'form-control input-perso'}),max_length=100,error_messages={'invalid': ("Email invalid.")})
        self.fields['password'] = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), help_text = '* Must contain at least 8 characters including a number')
        self.fields['password2'] = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
        # self.fields['country'] = forms.CharField(label='Country')
        # self.fields['city'] = forms.CharField(label='City')
        # self.fields['state'] = forms.CharField(label='State')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if umod.User.objects.filter(username=username).count() > 0:
            raise forms.ValidationError('This username is already taken. Could you already be signed up?')

        chars = ('0123456789 abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        for char in username:
            if char not in chars:
                raise forms.ValidationError('Usernames may only inlcude alphanumeric characters, numbers, and spaces.')
            
        return username


    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if umod.User.objects.filter(email=email).count() > 0:
            raise forms.ValidationError('This email is already taken. Could you already be signed up?')
        return email

    def clean_password(self):
        pw1 = self.cleaned_data.get('password')
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
        # ensure the passwords match
        if pw1 != pw2:
            raise forms.ValidationError('Please ensure the password fields match.')
        # return the cleaned data dict, per django spec
        return self.cleaned_data

    def commit(self):

        '''Process the form action'''
        u = umod.User()
        u.username = self.cleaned_data.get('username')
        u.email = self.cleaned_data.get('email')
        u.set_password(self.cleaned_data.get('password'))
        u.first_name = self.cleaned_data.get('first_name')
        u.last_name = self.cleaned_data.get('last_name')
        u.save()

        login(self.request, u, backend='django.contrib.auth.backends.ModelBackend')


        