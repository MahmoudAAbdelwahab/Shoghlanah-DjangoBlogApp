from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

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
	if not request.user.is_authenticated():
		raise PermissionDenied
	blog = Blog.objects.create(user=request.user)
	return redirect('show_blog', blog_id=blog.id)

def show_blog(request, blog_id):
	try:
		blog_item = Blog.objects.get(id=blog_id)
		list_of_blog_posts = Post.objects.filter(blog=blog_item)
		if request.user.is_authenticated():
			try:
				view = BlogView.objects.get(viewer=request.user, blog=blog_item)
			except BlogView.DoesNotExist:
				BlogView.objects.create(viewer=request.user, blog=blog_item)
				blog_item.increment_views()
			if request.user == blog_item.user:
				form = PostForm()
			else:
				form = None
			if Follow.objects.filter(follower=request.user, followed=blog_item.user):
				follow = True
			else:
				follow = False
		else:
			form = None
			follow = None
	except Blog.DoesNotExist:
		raise Http404
	except Post.DoesNotExist:
		list_of_blog_posts = None
	context = {'posts': list_of_blog_posts, 'blog': blog_item, 'form': form, 'follow': follow}
	return render(request, 'blog/show.html', context)

#def edit_blog

def delete_blog(request, blog_id):
	try:
		blog = Blog.objects.get(id=blog_id)
		if not request.user.is_authenticated() or request.user != blog.user:
			raise PermissionDenied
		else:
			blog.delete()
	except Blog.DoesNotExist:
		blog = None
	return redirect('index')

def create_post(request, blog_id):
	try:
		blog = Blog.objects.get(id=blog_id)
		if not request.user.is_authenticated() or request.user != blog.user:
			raise PermissionDenied
		post = Post.objects.create(user=request.user, blog=blog, title=request.POST['title'], content=request.POST['content'])
	except Blog.DoesNotExist:
		raise Http404
	return redirect('show_post', post_id=post.id)

def show_post(request, post_id):
	try:
		post_item = Post.objects.get(id=post_id)
		comments = Comment.objects.filter(post=post_item)
		if request.user.is_authenticated():
			form = CommentForm()
		else:
			form = None
	except Post.DoesNotExist:
		raise Http404
	context = {'post': post_item, 'comments': comments, 'form': form}
	return render(request, 'post/show.html', context)

def edit_post(request, post_id):
	try:
		post = Post.objects.get(id=post_id)
		if not request.user.is_authenticated() or request.user != post.user:
			raise PermissionDenied
		form = PostForm(instance=post)
	except Post.DoesNotExist:
		raise Http404
	context = {'post_id': post_id, 'form': form}
	return render(request, 'post/edit.html', context)

def update_post(request, post_id):
	try:
		posts = Post.objects.filter(id=post_id)
		if not request.user.is_authenticated() or request.user != posts[0].user:
			raise PermissionDenied
		posts.update(title=request.POST['title'], content=request.POST['content'])
	except Post.DoesNotExist:
		raise Http404
	return redirect('show_post', post_id=post_id)

def delete_post(request, post_id):
	try:
		post = Post.objects.get(id=post_id)
		blog = post.blog.id
		if not request.user.is_authenticated() or request.user != post.user:
			raise PermissionDenied
		post.delete()
	except Post.DoesNotExist:
		raise Http404
	return redirect('show_blog', blog_id=post.blog.id)

def add_comment(request, post_id):
	if not request.user.is_authenticated():
		raise PermissionDenied
	try:
		post_item = Post.objects.get(id=post_id)
	except Post.DoesNotExist:
		raise Http404
	Comment.objects.create(user=request.user, post=post_item, content=request.POST['content'])
	return redirect('show_post', post_id=post_id)

def follow(request, blog_id):
	if not request.user.is_authenticated():
		raise PermissionDenied
	try:
		Follow.objects.create(follower=request.user, followed=Blog.objects.get(id=blog_id).user)
	except Blog.DoesNotExist:
		raise Http404
	return redirect('show_blog', blog_id=blog_id)

def unfollow(request, blog_id):
	if not request.user.is_authenticated():
		raise PermissionDenied
	try:
		Follow.objects.get(follower=request.user, followed=Blog.objects.get(id=blog_id).user).delete()
	except:
		raise Http404
	return redirect('show_blog', blog_id=blog_id)