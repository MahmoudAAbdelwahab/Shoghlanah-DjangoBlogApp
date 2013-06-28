from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from blog.models import *

def login_user(request):
	try:
		user = User.objects.get(username=request.POST['username'])
		if user.check_password(request.POST['password']):
			user = authenticate(username=request.POST['username'], password=request.POST['password'])
			login(request, user)
	except User.DoesNotExist:
		user = None
	return redirect('index')	

def logout_user(request):
	logout(request)
	return redirect('index')

def index(request):
	print request.user
	if not request.user.is_authenticated():
		form = UserForm()
		return render(request, 'home/login.html', {'form': form})
	else:	
	    latest_blog_list = Blog.objects.order_by('-no_of_views')
    	context = {'blogs': latest_blog_list}
    	return render(request, 'blog/index.html', context)

def create_blog(request):
	blog = Blog.objects.create(user=User.objects.all()[2])
	return redirect('show_blog', blog_id=blog.id)

def show_blog(request, blog_id):
	try:
		blog_item = Blog.objects.get(id=blog_id)
		blog_item.increment_views()
		list_of_blog_posts = Post.objects.filter(blog=blog_item)
		form = PostForm()
	except Blog.DoesNotExist:
		raise Http404
	except Post.DoesNotExist:
		list_of_blog_posts = None
	context = {'posts': list_of_blog_posts, 'blog': blog_item, 'form': form}
	return render(request, 'blog/show.html', context)

#def edit_blog

def delete_blog(request, blog_id):
	try:
		blog = Blog.objects.get(id=blog_id).delete()
	except Blog.DoesNotExist:
		blog = None
	return redirect('index')

def create_post(request, blog_id):
	title = request.POST['title']
	content = request.POST['content']
	try:
		blog_item = Blog.objects.get(id=blog_id)
	except Blog.DoesNotExist:
		raise Http404
	post = Post.objects.create(user=blog_item.user, blog=blog_item, title=title, content=content)
	return redirect('show_post', post_id=post.id)

def show_post(request, post_id):
	try:
		post_item = Post.objects.get(id=post_id)
		comments = Comment.objects.filter(post=post_item)
		form = CommentForm()
	except Post.DoesNotExist:
		raise Http404
	context = {'post': post_item, 'comments': comments, 'form': form}
	return render(request, 'post/show.html', context)

#def edit_post

def delete_post(request, post_id):
	try:
		post = Post.objects.get(id=post_id)
		blog = post.blog.id
		post.delete()
	except Post.DoesNotExist:
		raise Http404
	return redirect('show_blog', blog_id=post.blog.id)

def add_comment(request, post_id):
	comment = request.POST['content']
	try:
		post_item = Post.objects.get(id=post_id)
	except Post.DoesNotExist:
		raise Http404
	Comment.objects.create(user=User.objects.all()[0], post=post_item, content=comment)
	return redirect('show_post', post_id=post_id)