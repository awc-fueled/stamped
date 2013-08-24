# Create your views here.
from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

# handle javascript varaible transfer 
import json
from django.core.serializers.json import DjangoJSONEncoder


from stamped.models import Restaurant, RestaurantForms



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
	# if request.method == 'POST':
	# 	restaurant = Restaurant.objects.filter(name='Fish', address='280 Bleecker St')
	# 	#check for an empty querry set
	# 	if len(restaurant) > 0:
	# 		upload_file(request) # might call render twice, need to test
	# 	else:
	# 		#get the object out of the list
	# 		restaurant = restaurant[0]
	# 	return render(request, "stamped/restaurant.html", {'restaurant': restaurant})
	# else:
	# 	sys.stdout.write("\n\nyouve beeen redirred\n\n")
	# 	return HttpResponseRedirect('/')
	restaurant = Restaurant.objects.filter(name='Fish', address='280 Bleecker St')[0]
	return render(request, "stamped/restaurant.html", {'restaurant': restaurant})

def upload_file(request):
    if request.method == 'POST':
        form = RestaurantForms(request.POST, request.FILES)
        if form.is_valid():
            # file is saved
            form.save()
            # render?
            return HttpResponseRedirect('/results/', {
            	'restaurant': get_object_or_404(
            									Restaurant, 
            									name=request.POST['name'], 
            									address=request.POST['address']
            									)
            	})
    else:
        form = RestaurantForms()
    return render(request, 'stamped/formtest.html', {'form': form})

def custom_tag(request):
	import datetime 

	d = datetime.datetime(2013,3,5)
	return render(request, 'stamped/customtag.html', {'d': d})
	