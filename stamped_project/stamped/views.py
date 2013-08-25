# Create your views here.
from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import permission_required, login_required

from stamped.models import Restaurant, RestaurantForm, CommentForm, CreateUserForm, Review



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
	recently_added_Restaurants = Restaurant.objects.order_by("date_added")[:5]
	recent_reviews = Review.objects.order_by("date_added")
	return render(request, "stamped/home.html", {
		'top_choices': top_choices, 
		'recently_added_Restaurants': recently_added_Restaurants, 
		'recent_reviews':recent_reviews,
		} )
	
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

@permission_required('user_meta.add_restaurant')
def upload_file(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES)
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
        form = RestaurantForm()
    return render(request, 'stamped/formtest.html', {'form': form})

def custom_tag(request):
	import datetime 

	d = datetime.datetime(2013,3,5)
	return render(request, 'stamped/customtag.html', {'d': d})

@login_required
def make_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
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
        form = CommentForm()
    return render(request, 'stamped/comment.html', {'form': form})





# from django.contrib.auth import authenticate, login
# def login_view(request):
#     username = request.POST['username']
#     password = request.POST['password']
#     user = authenticate(username=username, password=password)
#     if user is not None:
#         if user.is_active:
#             login(request, user)
#             # Redirect to a success page.
#         else:
#             # Return a 'disabled account' error message
#     else:
#         # Return an 'invalid login' error message.

from django.contrib.auth import logout
def logout_view(request):
    logout(request)

def create_user(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST, request.FILES)
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
        form = CreateUserForm()
    return render(request, 'stamped/create_user.html', {'form': form})
