# Create your views here.
from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

# handle javascript varaible transfer 
import json
from django.core.serializers.json import DjangoJSONEncoder


from stamped.models import Restaurant

def home(request):
	return render(request, "stamped/home.html")

def results(request):
	# import sys
	# sys.stdout.write("\nresults view action\n")
	# sys.stdout.write(result){'result':result}
	#context = get_object_or_404(Restaurant, pk=1)
	#restaurant.review_set.all()
	return render(request, "stamped/restaurant.html")