# Create your views here.
from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

# handle javascript varaible transfer 
import json
from django.core.serializers.json import DjangoJSONEncoder


from stamped.models import Restaurant



def home(request):
	category_choices = [
					('american', 'American'),
					('bar_food', 'Bar Food'),
					('seafood', 'Seafood'),
					('sandwiches', 'Sandwiches'),
					('french', 'French'),
					('comfortfood', 'Comfort Food'),
					('suhi', 'Sushi Bar'),
					('unknown_cat', 'To cool to be defined')	
				]
	
	import random
	top_choices = []
	for i in xrange(0, 3):
		category = random.choice(category_choices)
		top_5 = Restaurant.objects.filter(category=category[0]).order_by('rating')[:5]
		top_choices.append(top_5)
	import sys; sys.stdout.write(str(len(top_choices)))	
	return render(request, "stamped/home.html", {'top_choices': top_choices} )
	
def results(request):
	# import sys
	# sys.stdout.write("\nresults view action\n")
	# sys.stdout.write(result){'result':result}
	restaurant = get_object_or_404(Restaurant, name='Fish', address='280 Bleecker St')
	return render(request, "stamped/restaurant.html", {'restaurant': restaurant})

