from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from formlib import Formless
from django import forms
from users import models as umod
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
import re
import random
from urllib.parse import urlsplit


@view_function
def process_request(request):

    # process the form
    form = ForgotForm(request)
    form.submit_text = 'Submit'
    if form.is_valid():
        form.commit()
        return HttpResponseRedirect('/accounts/forgot_password_confirm')

    # render the template
    return request.dmp.render('forgot_password.html', {
        'form': form,
    })


class ForgotForm(Formless):
    def init(self):
        '''Adds the fields for this form'''
        self.fields['email1'] = forms.EmailField(label="", widget=forms.EmailInput(attrs={'placeholder': 'Email','class':'form-control input-perso'}),error_messages={'invalid': ("Email invalid.")})
        self.fields['email2'] = forms.EmailField(label="", widget=forms.EmailInput(attrs={'placeholder': 'Confirm Email','class':'form-control input-perso'}),error_messages={'invalid': ("Email invalid.")})
    
    def clean_email(self):
        email = self.cleaned_data.get('email1')
        if umod.User.objects.get(email=email):
            return email
        else:
            raise forms.ValidationError('This email is not connected to any current accounts.')
        

    def clean(self):
        email1 = self.cleaned_data.get('email1')
        email2 = self.cleaned_data.get('email2')
        # ensure the passwords match
        if email1 != email2:
            raise forms.ValidationError('Please ensure the emails match.')
        # return the cleaned data dict, per django spec
        return self.cleaned_data

    def commit(self):
        '''Process the form action'''
        email = self.cleaned_data.get('email1')

        def generateToken():
            string_pieces = "0123456789abcdejghijklmnopqrstuvwxyz"
            token_size = random.randrange(50,75)
            token = ""
            for _ in range(token_size):
                token += string_pieces[random.randrange(len(string_pieces))]
            # print('-----------------------------', token)
            u = umod.User.objects.get(email=email)
            t = umod.ResetPasswordTokens()
            t.token = token
            t.user_id = u.id
            t.save()

            return token



        url = self.request.build_absolute_uri()
        base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url))


        send_mail('Hello', "Here is your password reset token:\n\n" + base_url + "accounts/forgot_password_token/" + generateToken() + "\n\nKeep on Reading!", 'bookvotingapp@gmail.com', [email])
