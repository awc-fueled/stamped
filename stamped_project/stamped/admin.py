from django.contrib import admin
from stamped.models import Restaurant, Review, Comment, User_Meta

admin.site.register(Restaurant)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(User_Meta)
