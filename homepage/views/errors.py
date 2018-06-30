from django.conf import settings
from django_mako_plus import view_function


@view_function
def not_found(request, exception=None):


    context = {
    }
    return request.dmp.render('404.html', context)

@view_function
def server_error(request, exception=None):


    context = {
    }
    return request.dmp.render('500.html', context)