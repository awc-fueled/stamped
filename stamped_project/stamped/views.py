# Create your views here.
from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth import logout, authenticate, login

from stamped.models import Restaurant, Review, RestaurantForm, CommentForm, CreateUserForm, CreateUser_MetaForm, ReviewForm


### basic website navigation views #####
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
		top_5 = sorted(Restaurant.objects.filter(category=category[0]), key=lambda x: x.rating)[:5]
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

##### Handle views with uploading files / adding information to database ######
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
    return render(request, 'stamped/upload_file.html', {'form': form})

@login_required
def make_comment(request):
    if request.method == 'POST':
    	print request.POST
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
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

@login_required
def add_review(request):
    if request.method == 'POST':
    	print request.POST
        form = ReviewForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            # render?
            return HttpResponseRedirect('/results/', {
            	'restaurant': get_object_or_404(
            									Restaurant, 
            									name=request.POST['name'], 
            									address=request.POST['address']
            									)
            	})
    else:
        form = ReviewForm()
    return render(request, 'stamped/comment.html', {'form': form})




##### Handle Login/Log out views ####
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


def logout_view(request):
    logout(request)

def create_user(request):
	'''
	create and login user
	'''
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			# file is saved
			form.save()
			#login user
			username = form['username']
			password = form['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
			    	return HttpResponseRedirect('/create_user_meta/')
	else:
		form = CreateUserForm()
	return render(request, 'stamped/create_user.html', {'form': form})

def create_user_meta(request):
    if request.method == 'POST':
        form = CreateUser_MetaForm(request.POST, request.FILES)
        if form.is_valid():
            user_meta = form.save(commit=False)
            user_meta.user = request.user
            form.save()
            
            return HttpResponseRedirect('/')
    else:
        form = CreateUser_MetaForm()
    return render(request, 'stamped/create_user_meta.html', {'form': form})
