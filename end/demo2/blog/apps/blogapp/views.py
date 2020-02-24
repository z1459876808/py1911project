from django.shortcuts import render, redirect, reverse
from .models import *
# Django自带分页和分页器
from django.core.paginator import Page, Paginator

# Page中有 objects_list 代表当前页的所有对象
# has_next 是不是有下一页
# has_previous 是否有上一页
# next_page_number 下一 页的编号
# previous_page_number 上一页的编号
# self.number当前页的编号
# self.paginator当的页的分页器

# Paginator objects_list 代表所有未分页对象
# self.per. page每一页有几个对象
# get_page(self, number): 从分页器中取第几页
# page_range(self):返回分页列表


# Create your views here.
from django.http import HttpResponse
from .forms import *


def index(request):
    ads = Ads.objects.all()

    typepage = request.GET.get('typepage')
    year = None
    month = None
    if typepage == 'date':
        year = request.GET.get('year')
        month = request.GET.get('month')
        articles = Article.objects.filter(create_time__year=year, create_time__month=month).order_by('-create_time')
    elif typepage == 'category':
        category_id = request.GET.get('category_id')
        try:
            category = Category.objects.get(id=category_id)
            articles = category.article_set.all()
        except Exception as e:
            print(e)
            return HttpResponse('分类不合法')
    elif typepage == 'tag':
        tag_id = request.GET.get('tag_id')
        try:
            tag = Tag.objects.get(id=tag_id)
            articles = tag.article_set.all()
        except Exception as e:
            print(e)
            return HttpResponse('标签不合法')
    else:
        articles = Article.objects.all().order_by('-create_time')

    paginator = Paginator(articles, 1)
    num = request.GET.get('pagenum', 1)
    page = paginator.get_page(num)

    lates3article = articles.order_by('create_time')[:3]

    # locals()可以返回作用域的局部变量
    return render(request, 'index.html', {'ads': ads, 'page': page, 'type': typepage, 'year': year, 'month': month})


def detail(request, articleid):
    # return HttpResponse("详情")
    if request.method == "GET":
        try:
            article = Article.objects.get(id=articleid)
            cf = CommentForm()
            return render(request, 'single.html', locals())
        except Exception as e:
            print(e, "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            return HttpResponse("文章不合法")
    elif request.method == "POST":
        cf = CommentForm(request.POST)
        if cf.is_valid():
            print(cf)
            comment = cf.save(commit=False)
            comment.article = Article.objects.get(id=articleid)
            comment.save()
            url = reverse("blogapp:detail", args=(articleid,))
            return redirect(to=url)
        else:
            article = Article.objects.get(id=articleid)
            cf = CommentForm()
            errors = "输入信息有误"
            return render(request, "single.html", locals())


def contact(request):
    return render(request, 'contact.html')


def favicon(request):
    return redirect(to='/static/favicon.ico')
