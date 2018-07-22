from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django_mako_plus import view_function


@view_function
def process_request(request):

    # render the template
    return request.dmp.render('privacy_policy.html')
