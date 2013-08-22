from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Restaurant(models.Model):
	name = models.CharField(max_length=200)
	address = models.CharField(max_length=200)
	stamped_out =  models.BooleanField(default=False)
	profile_picture = models.ImageField(upload_to='restaurants_profile_pictures/', blank=True, null=True)
	date_added = models.DateTimeField(auto_now_add=True)

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
	can_add_restaurants = models.BooleanField(default=False)
	avg_review = models.FloatField()

	def __unicode__(self):
		'''
		for human readable model representation 
		'''
		return "User: %s, Add restaurant?%s" %(self.user, self.can_add_restaurants)