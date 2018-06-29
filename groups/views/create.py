from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from groups import models as gMod
from formlib import Formless
from django import forms
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect


@view_function
@login_required
def process_request(request):
    
    # process the form
    form = CreateForm(request)
    if form.is_valid():
        form.commit()
        return HttpResponseRedirect('/')

    context = {
        'form': form,
    }
    return request.dmp.render('create.html', context)

class CreateForm(Formless):
    def init(self):
        '''Adds the fields for this form'''
        self.fields['name'] = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Group Name'}))
        self.fields['description'] = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': 'Description'}), required=False)
        self.fields['is_private'] = forms.BooleanField(label='Private Group', initial=True, required=False)

    def clean(self):
        try:
            group = gMod.Group.objects.get(name = self.cleaned_data.get('name'))
            raise forms.ValidationError('This Group Name already exists please choose another.')
        except:
            return self.cleaned_data

    def commit(self):
        '''Process the form action'''
        g = gMod.Group()
        g.name = self.cleaned_data.get('name')
        g.description = self.cleaned_data.get('description')
        g.is_private = self.cleaned_data.get('is_private')
        g.save()
        
        g.users.add(self.request.user)
        g.admin_users.add(self.request.user)
        