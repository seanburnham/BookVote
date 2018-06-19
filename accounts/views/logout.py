from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from formlib import Formless
from django import forms
from users import models as umod
import re


@view_function
def process_request(request):
    # log the user out
    logout(request)

    # redirect to the home page
    return HttpResponseRedirect('/')
