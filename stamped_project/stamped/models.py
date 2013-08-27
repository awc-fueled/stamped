from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm, HiddenInput



class Restaurant(models.Model):
	# define restaurant categories 		
	category_choices = [
					('asian', 'Asian'),
					('american', 'American'),
					('bar_food', 'Bar Food'),
					('seafood', 'Seafood'),
					('sandwiches', 'Sandwiches'),
					('french', 'French'),
					('comfortfood', 'Comfort Food'),
					('suhi', 'Sushi Bar'),
					('unknown_cat', 'To cool to be defined')	
				]	
	name = models.CharField(max_length=200)
	address = models.CharField(max_length=200)
	category = models.CharField(max_length=200,
                                choices=category_choices,
                                default='unknown_cat')
	
	stamped_out_count = models.IntegerField()
	profile_picture = models.ImageField(upload_to='restaurants_profile_pictures/', blank=True, null=True)
	date_added = models.DateTimeField(auto_now_add=True)
	
	@property
	def stamped_out(self):
		s_count = Restaurant.objects.get(pk=self.id).stamped_out_count
		u_count = User.objects.count()
		if s_count > (u_count * 0.1):
			return True
		else:
			return False

	@property
	def rating(self):
	 	from django.db.models import Avg
	 	return Review.objects.filter(restaurant=self.id).aggregate(Avg('rating'))['rating__avg']

	def __unicode__(self):
		'''
		for human readable model representation 
		'''
		return self.name

class Review(models.Model):
	content = models.TextField()
	rating = models.IntegerField()
	user = models.ForeignKey(User)
	restaurant = models.ForeignKey(Restaurant)
	date_added = models.DateTimeField(auto_now_add=True)

	@property 
	def avg_rating(self):
		from django.db.models import Avg
		return Review.objects.all().aggregate(Avg('rating'))['rating__avg']
		

	def __unicode__(self):
		'''
		for human readable model representation 
		'''	
		return "Review of %s by %s on %s" %(self.restaurant, self.user, self.date_added)

class Comment(models.Model):
	content = models.TextField()
	review = models.ForeignKey(Review)
	user = models.ForeignKey(User)
	date_added = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		'''
		for human readable model representation 
		'''
		return "Comment %s's review of %s on %s" %(self.user, self.review.restaurant, self.date_added)

class User_Meta(models.Model):
	user = models.OneToOneField(User)
	profile_picture = models.ImageField(upload_to='user_profile_pictures/', blank=True, null=True)
	bio = models.TextField()

	@property
	def avg_rating(self):
		from django.db.models import Avg
		return Review.objects.filter(user=self.user).aggregate(Avg('rating'))

	def __unicode__(self):
		'''
		for human readable model representation 
		'''
		return "User: %s, Can I add restaurants? [%s]" %(self.user, self.user.has_perm('add_resturant'))



#### ModelForms ####
class RestaurantForm(ModelForm):
	class Meta:
		model = Restaurant 

class ReviewForm(ModelForm):
	class Meta:
		model = Review 
		exclude = ('user',)
		widgets = {'restaurant': HiddenInput()}

class CommentForm(ModelForm):
	class Meta:
		model = Comment
		exclude = ('user',)
		widgets = {'review': HiddenInput()}

class CreateUserForm(ModelForm):
	class Meta:
		model = User
		fields = ('username', 'password', 'first_name', 'last_name', "email")

class CreateUser_MetaForm(ModelForm):
	class Meta:
		model = User_Meta
		exclude = ('user','avg_review')


