# Create your views here.
from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Permission

from stamped.models import Restaurant, Review, Comment, RestaurantForm, CommentForm, CreateUser_MetaForm, ReviewForm


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
		top_5 = sorted(Restaurant.objects.filter(category=category[0]), key=lambda x: x.rating, reverse=True)[:5]
		top_choices.append(top_5)
	recently_added_Restaurants = Restaurant.objects.order_by("date_added")[:5]
	recent_reviews = Review.objects.order_by("date_added")[:5]
	recent_comments = Comment.objects.order_by("date_added")[:5]
	return render(request, "stamped/base.html", {
		'top_choices': top_choices, 
		'recently_added_Restaurants': recently_added_Restaurants, 
		'recent_reviews':recent_reviews,
		'recent_comments': recent_comments,
		} )

def results(request):
	from django.shortcuts import redirect
	from django.http import Http404
	print request
	if request.method == 'POST':
		print request.POST
		name=request.POST.get('name')
		address=request.POST.get('address')
		try:
			print "lookedup"
			restaurant = get_object_or_404(Restaurant, name=name, address=address)
			print restaurant
			return render(request, "stamped/restaurant.html", {'restaurant': restaurant, 'x':True})
		except Http404,e: 
				print str(e)
				print "exception!"			
				if 'category' in request.POST:
					form = RestaurantForm(request.POST, request.FILES)
					if form.is_valid():
						restaurant = form.save(commit=False)
						#set intial stamped out count to zero
						restaurant.stamped_out_count = 0
						restaurant.save()
						restaurant = get_object_or_404(Restaurant, name=name, address=address)
						return render(request, "stamped/restaurant.html", {'restaurant': restaurant})
				else:
					form = RestaurantForm(initial={'name':name, 'address':address})
				return render(request, 'stamped/add_restaurant.html', {'form': form, 'name': name, 'address': address})

	
##### Handle views with uploading files / adding information to database ######
@permission_required('user_meta.add_restaurant')
def add_restaurant(request, name, address):
	print "\nFirst \n"
	print request
	if request.method == 'POST':
		if 'category' in request.POST:
			print "not name or address"
			form = RestaurantForm(request.POST, request.FILES)
			form.stamped_out_count = 0
			print form.stamped_out_count
			print "is form valid?"
			print form.is_valid()
			print form.errors.items()
			print form.category
			print form.errors
			if form.is_valid():
				print request.POST
				form.save()
				return HttpResponseRedirect('/results/', {
				'restaurant': get_object_or_404(
												Restaurant, 
												name=request.POST['name'], 
												address=request.POST['address']
												)
				})
	else:
		print request.POST
		print request.GET
		print 'name / addres'
		print name, address
		print args
		form = RestaurantForm(initial={'name':name, 'address':address})
	return render(request, 'stamped/add_restaurant.html', {'form': form, 'name': name, 'address': address})

@login_required
def add_comment(request):
	if request.method == 'POST':	
		if 'prepair_comment' in request.POST:
			review = get_object_or_404(Review, pk=request.POST.get('review_id'))
			form = CommentForm({'review': review.id})
			return render(request, 'stamped/comment.html', {
				'form': form,
			})
		
		form = CommentForm(request.POST)
		if form.is_valid():
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

def decay_choice(choices, val):
    #for each additional 10,000 users, remove a percentage
    #chance for a single user to get the add_restaurant 
    #privlage stops assigning admins at 1,000,000 users 
    #where app should be self sufficent

    import random
    penalty = val // 10000
    #control for values that might exceed 100
    if penalty >= 100:
        penalty = 100
    print penalty
    choices[0][1] -= penalty
    choices[0][1] += penalty
    #get a random number from a uniform distribution
    r = random.uniform(0, 100)
    if r <= choices[0][1]:
        return choices[0][0]
    elif r <= choices[1][1]:
        return choices[1][1]

def can_add_restaurants(user):
	'''
	Assign's permsion to add houses as a piecwise decay function.

	Initially, the app will assign all users as admins, those that 
	can add houses, until the user base reaches 1000. As the app grows 
	the amount of admins assigned per user registration shrinks. 
	Resutlting in a large userbase with realtively few admins. As the 
	user base changes, the function will assign more or less admins. In 
	this way it ensures that there are always enough admins to keep the site
	going.  

	'''

	user_count = User.objects.count()

	if user_count > 1000:
		user.user_permissions.add('add_restaurant')
	elif user_count < 1000:
		#intial proportions of users to admin
		#actually 90 10 because it will only 
		#be called at the 1000 user level
		choices = [[1,91], [0,9]]
		add_bool = decay_choice(choices, user_count)
		if add_bool == 1:
			p = Permission.objects.get(codename='add_restaurant')
			user.user_permissions.add(p)

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
					# Assing add_restaurant permission
					can_add_restaurants(user)
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
