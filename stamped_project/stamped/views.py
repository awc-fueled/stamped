# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

# handle javascript varaible transfer 
import json
from django.core.serializers.json import DjangoJSONEncoder

#from stamped.models import 

def home(request):
	return HttpResponse("Hello, world.")