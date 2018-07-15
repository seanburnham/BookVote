from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from users import models as umod
from urllib import parse
from formlib import Formless
from django import forms
from urllib.parse import urlsplit
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
import random
import re

resetToken = None

@view_function
def process_request(request, token):
    
    global resetToken
    resetToken = token
    
    verifiedToken = False
    message = ""
    try:
        verifiedToken = umod.ResetPasswordTokens.objects.get(token = token)
    except:
        message = "This token is an inaccurate token or has already been used."


    form = ResetPasswordForm(request)
    if form.is_valid():
        form.commit()
        return HttpResponseRedirect("/accounts/login")
            


    context = {
        'verifiedToken': verifiedToken,
        'message': message,
        'form': form,
    }

    # render the template
    return request.dmp.render('forgot_password_token.html', context)



class ResetPasswordForm(Formless):
    def init(self):
        self.fields['password'] = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'New Password'}), help_text = '* Must contain at least 8 characters including a number')
        self.fields['password2'] = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Confirm New Password'}))

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
        global resetToken
        token = umod.ResetPasswordTokens.objects.get(token=resetToken)

        u = umod.User.objects.get(id=token.user_id)
        t_list = umod.ResetPasswordTokens.objects.filter(user_id = u.id)

        password = self.cleaned_data.get('password')
        u.set_password(password)
        u.save()

        for t in t_list:
            t.delete()