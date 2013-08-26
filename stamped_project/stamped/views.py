# Create your views here.
from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm

from stamped.models import Restaurant, Review, RestaurantForm, CommentForm, CreateUser_MetaForm, ReviewForm


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
		# using sorted here becuase rating is a property and not a database column
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
def add_comment(request):
	if request.method == 'POST':	
		if 'prepair_comment' in request.POST:
			print request.POST
			review = get_object_or_404(Review, pk=request.POST.get('review_id'))
			form = CommentForm({'review': review.id})
			return render(request, 'stamped/comment.html', {
				'form': form,
			})
		
		form = CommentForm(request.POST)
		if form.is_valid():
			print "form is valid"
			comment = form.save(commit=False)
			comment.user = request.user
			comment.save()
			return HttpResponseRedirect('/results/')
			# return HttpResponseRedirect('/results/', {
			# 	'restaurant': get_object_or_404(
			# 									Restaurant, 
			# 									name=request.POST['name'], 
			# 									address=request.POST['address']
			# 									)
			# 	})
	else:
		form = CommentForm()
	return render(request, 'stamped/comment.html', {'form': form})

@login_required
def add_review(request):
	'''
	adds a review for a restaurant to the database
	'''
	if request.method == 'POST':	
		if 'prepair_review' in request.POST:
			print request.POST
			restaurant = get_object_or_404(Restaurant, pk=request.POST.get('rest_id'))
			form = ReviewForm({'restaurant': restaurant.id})
			return render(request, 'stamped/comment.html', {
				'form': form,
			})
		
		form = ReviewForm(request.POST)
		if form.is_valid():
			print "form is valid"
			review = form.save(commit=False)
			review.user = request.user
			review.save()
			return HttpResponseRedirect('/results/')
			# return HttpResponseRedirect('/results/', {
			# 	'restaurant': get_object_or_404(
			# 									Restaurant, 
			# 									name=request.POST['name'], 
			# 									address=request.POST['address']
			# 									)
			# 	})
	else:
		form = ReviewForm()
	return render(request, 'stamped/comment.html', {'form': form})

def stamp_out(request):
	'''
	increment stamped out count
	'''
	if request.method == 'POST':	
		if 'prepair_stamp_out' in request.POST:
			r = Restaurant.objects.get(pk=request.POST.get('rest_id'))
			r.stamped_out_count += 1
			r.save()
			return HttpResponseRedirect('/results/')
	
	return HttpResponseRedirect('/')



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
		form = UserCreationForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password2')
			form.save()
			#login user
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
			    	return HttpResponseRedirect('/create_user_meta/')
	else:
		form = UserCreationForm()
	return render(request, 'stamped/create_user.html', {'form': form})

def create_user_meta(request):
    if request.method == 'POST':
        form = CreateUser_MetaForm(request.POST)
        if form.is_valid():
            user_meta = form.save(commit=False)
            user_meta.user = request.user
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = CreateUser_MetaForm()
    return render(request, 'stamped/create_user_meta.html', {'form': form})
