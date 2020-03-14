from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from django.shortcuts import get_object_or_404, render
import markdown
import re
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify
from .models import Tag, Post, Category
# Create your views here.

def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    return  render(request, 'blog/index.html', context={
        'post_list' : post_list
    })

# 翻页函数
def detail(request, pk):
    post = get_object_or_404(Post, pk = pk)
    md = markdown.Markdown(extensions = [
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                        TocExtension(slugify=slugify),
                                  ])
    post.body = md.convert(post.body)
    if not request.COOKIES.get("pk_id:{}".format(pk)):
        post.read_num +=1
        post.save()
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''
    respons = render(request, 'blog/detail.html', context={'post':post})
    respons.set_cookie("pk_id:{}".format(pk),'True')
    return respons

def archive(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})

def category(request, pk):
    # 记得在开始部分导入 Category 类
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})

def tag(request, pk):
    # 记得在开始部分导入 Category 类
    t = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=t).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})




