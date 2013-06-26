from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model):
	user = models.OneToOneField(User)
	no_of_views = models.IntegerField(default=0)

	def increment_views(self):
		self.no_of_views += 1

class Post(models.Model):
	user = models.ForeignKey(User)
	blog = models.ForeignKey(Blog)
	content = models.CharField(max_length=1000)

class Comment(models.Model):
	user = models.ForeignKey(User)
	post = models.ForeignKey(Post)
	content = models.CharField(max_length=140)

class Follow(models.Model):
	follower = models.ForeignKey(User, related_name='follower')
	followed = models.ForeignKey(User, related_name='followed')

	class Meta:
		unique_together = ('follower', 'followed')