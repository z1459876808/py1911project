from django.shortcuts import render, redirect, reverse
from django.template import loader

# Create your views here.


from django.http import HttpResponse
from .models import Book, Hero


def index(request):
    # return HttpResponse('这里是首页')

    # 1、获取模板
    # template = loader.get_template('index.html')
    # 2、渲染模板数据
    books = Book.objects.all()
    # context = {'books': books}
    # result = template.render(context)
    # 3、将渲染得结果使用HttpResponse返回
    # return HttpResponse(result)

    return render(request, 'index.html', {'books': books})


def about(request):
    return HttpResponse('这里是关于')


def detail(request, bookid):
    # template = loader.get_template('detail.html')
    book = Book.objects.get(id=bookid)
    # context = {'book': book}
    # resault = template.render(context)
    # return HttpResponse(resault)

    return render(request, 'detail.html', {'book': book})


def deletebook(request, bookid):
    book = Book.objects.get(id=bookid)
    book.delete()
    return redirect(to='/')


def deletehero(request, heroid):
    hero = Hero.objects.get(id=heroid)
    bookid = hero.book.id
    hero.delete()
    url = reverse("booktest:detail", args=(bookid,))
    return redirect(to=url)


def addbook(requset):
    if requset.method == 'GET':
        return render(requset, 'addbook.html')
    elif requset.method == 'POST':
        book = Book()
        book.title = requset.POST.get('booktitle')
        book.pub_date = requset.POST.get('bookdate')
        book.price = requset.POST.get('bookprice')
        book.save()
        url = reverse('booktest:index')
        return redirect(to=url)


def editbook(requset, bookid):
    book = Book.objects.get(id=bookid)
    if requset.method == 'GET':
        return render(requset, 'editbook.html', {'book': book})
    elif requset.method == 'POST':
        book.title = requset.POST.get('booktitle')
        book.pub_date = requset.POST.get('bookdate')
        book.price = requset.POST.get('bookprice')
        book.save()
        return redirect(to='/')


def addhero(request, bookid):
    if request.method == 'GET':
        return render(request, 'addhero.html')
    elif request.method == 'POST':
        hero = Hero()
        hero.name = request.POST.get('heroname')
        hero.content = request.POST.get('herocontent')
        hero.gender = request.POST.get('sex')
        hero.book = Book.objects.get(id=bookid)
        hero.save()
        url = reverse('booktest:detail', args=(bookid,))
        return redirect(to=url)


def edithero(request, heroid):
    # 使用get方法进入英雄编辑页面
    hero = Hero.objects.get(id=heroid)
    if request.method == 'GET':
        return render(request, 'edithero.html', {'hero': hero})
    elif request.method == 'POST':
        hero.name = request.POST.get('heroname')
        hero.content = request.POST.get('herocontent')
        hero.gender = request.POST.get('sex')
        hero.save()
        url = reverse('booktest:detail', args=(hero.book.id,))
        return redirect(to=url)
