from django.shortcuts import render
 
from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone

@view_function
def process_request(request):
	return render(request, 'test.html')