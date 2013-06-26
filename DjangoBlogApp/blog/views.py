from django.shortcuts import render

from blog.models import Blog

def index(request):
    latest_blog_list = Blog.objects.order_by('user')
    context = {'latest_blog_list': latest_blog_list}
    return render(request, 'blog/index.html', context)