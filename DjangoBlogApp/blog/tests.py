"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase, client
from django.http import Http404
from django.contrib.auth.models import User

class BlogViewTests(TestCase):
	def setUp(self):
		"""
		Creates a new user in the database
		"""
		user = User.objects.create_user(username='mahmoudhashish', password='mahmoudhashish')

	def test_login(self):
		"""
		Tests that login functions well, and that the client has been successfully entered to the session/response
		"""
		self.client.login(username='mahmoudhashish', password='mahmoudhashish')
		response = self.client.get('/blog/')
		self.assertEqual(response.client, self.client)

	def test_index_view_without_blogs(self):
		"""
		Tests that the index view shows a certain message when it has no blogs
		"""
		self.test_login()
		response = self.client.get('/blog/')
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'No blogs are available.')

	def test_index_view_with_blogs(self):
		"""
		Tests that the index view shows a certain message when it has no blogs
		"""
		self.test_create_blog()
		response = self.client.get('/blog/')
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'mahmoudhashish')


	def test_show_blog(self):
		"""
		Tests that a certain message will be shown in a blog view
		"""
		self.test_create_blog()
		response = self.client.get('/blog/1/')
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "mahmoudhashish's blog")		

	def test_create_blog(self):
		"""
		Tests create blog funtionality, when the blog is created the response is a redirect to the show blog view
		"""
		self.test_login()
		response = self.client.get('/blog/create/')
		self.assertEqual(response.status_code, 302)
		response = self.client.get('/blog/1/')
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "mahmoudhashish's blog")		

	def test_delete_blog(self):
		"""
		Tests delete blog funtionality, when the blog is delete the response is a redirect to the index blog view
		"""
		self.test_create_blog()
		response = self.client.get('/blog/1/delete/')
		self.assertEqual(response.status_code, 302)
		response = self.client.get('/blog/')
		self.assertEqual(response.status_code, 200)
		self.assertNotContains(response, 'mahmoudhashish')		

	def test_create_post(self):
		"""
		Tests create post funtionality, when the post is created the response is a redirect to the show post view
		"""
		self.test_create_blog()
		response = self.client.post('/blog/1/post/create/', {'title': 'post title', 'content': 'post content'})
		self.assertEqual(response.status_code, 302)
		response = self.client.get('/blog/post/1/')
		self.assertContains(response, 'post title')
		self.assertContains(response, 'post content')

	def test_show_post(self):
		"""
		Tests that the post title will be shown in the show post view
		"""
		self.test_create_post()
		response = self.client.get('/blog/post/1/')
		self.assertContains(response, 'post')

	def test_edit_post(self):
		"""
		Tests edit post funtionality, when the post is edited the response is a redirect to the show post view,
		it also makes sure that the new data have been entered
		"""
		self.test_create_post()
		response = self.client.post('/blog/post/1/update/', {'title': 'post title edit', 'content': 'post content edit'})
		self.assertEqual(response.status_code, 302)
		response = self.client.get('/blog/post/1/')
		self.assertContains(response, 'post title edit')
		self.assertContains(response, 'post content edit')

	def test_delete_post(self):
		"""
		Tests delete post funtionality, when the blog is delete the response is a redirect to the show blog view
		"""
		self.test_create_post()
		response = self.client.get('/blog/post/1/delete/')
		self.assertEqual(response.status_code, 302)
		response = self.client.get('/blog/1/')
		self.assertNotContains(response, 'post title')
		self.assertNotContains(response, 'post content')

	def test_add_comment(self):
		"""
		Tests add comment funtionality, when the comment is added the response is a redirect to the show post view
		"""
		self.test_create_post()
		response = self.client.post('/blog/post/1/comment/add/', {'content': 'comment'})
		self.assertEqual(response.status_code, 302)
		response = self.client.get('/blog/post/1/')
		self.assertContains(response, 'comment')

	def test_follow(self):
		"""
		Tests follow funtionality, when a user follows another the response is a redirect to the show blog view
		"""
		self.test_create_blog()
		response = self.client.get('/blog/1/follow/')
		self.assertEqual(response.status_code, 302)
		response = self.client.get('/blog/1/')
		self.assertContains(response, 'unfollow')
		
	def test_unfollow(self):
		"""
		Tests unfollow funtionality, when a user unfollows another the response is a redirect to the show blog view
		"""
		self.test_follow()
		response = self.client.get('/blog/1/unfollow/')
		self.assertEqual(response.status_code, 302)
		response = self.client.get('/blog/1/')
		self.assertContains(response, 'follow')
		self.assertNotContains(response, 'unfollow')

	def test_logout(self):
		"""
		Tests that logout functions well, and that the client has been successfully removed from the session/response
		"""
		self.test_login()
		self.client.logout()
		response = self.client.get('/blog/')
		self.assertContains(response, 'login')