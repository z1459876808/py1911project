from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse, FileResponse
from .models import *
# Create your views here.
from django.views.generic import View, TemplateView, ListView, CreateView, DeleteView, UpdateView, DetailView as DV
# View类为所有的视图响应类的父类
from django.contrib.auth import authenticate, login as lin, logout as lot
from .forms import LoginFrom, RegistFrom


def index(request):
    print("====================")
    print(request.GET.get("hobbys"))
    print(request.GET.getlist("hobbys"))
    # print(request.META.get('HTTP_X_REQUESTED_WITH'))
    # print(dir(request))

    questions = Question.objects.all()
    # 使用render发起一次请求
    return render(request, 'polls/index.html', {"questions": questions})
    # return HttpResponse("首页")
    # return JsonResponse({"name":"zzy"})

    # return FileResponse(open("static/img/公众号.jpg","rb"),content_type="image/png",filename="aa.png",as_attachment=True)


# 基于CBV的形式实现首页
class IndexView(ListView):
    # 方法二、继承ListView
    # template_name指明使用的模板
    template_name = "polls/index.html"
    # queryset 指明返回的结果列表
    queryset = Question.objects.all()
    # context_object_name 指明返回字典参数的健
    context_object_name = "questions"

    # 方法一、继承的TemplateView
    # template_name = "polls/index.html"
    # def get_context_data(self, **kwargs):
    #     return {"questions":Question.objects.all()}


def detail(request, qid):
    print(qid, "+++")
    if request.method == "GET":
        print("当前用户", request.user.username)
        if request.user and request.user.username != "":
            # 已经登录过了
            # print("++",request.user.questions,type(request.user.questions.all()))
            try:
                question = Question.objects.get(id=qid)
                if question in request.user.questions.all():
                    print("已经投过票")
                    url = reverse("polls:result", args=(qid))
                    return redirect(to=url)
                else:
                    try:
                        # question = Question.objects.get(id=qid)
                        print(question, "--")
                        # 使用render发起一起请求
                        return render(request, 'polls/detail.html', {"question": question})

                    except Exception as e:
                        print(e, "--")
                        return HttpResponse("问题不合法")

            except Exception as e:
                print(e, "-----")

        else:
            url = reverse("polls:login") + "?next=/polls/detail/" + qid + "/"
            return redirect(to=url)
    elif request.method == "POST":
        choiceid = request.POST.get("num")
        # try:
        choice = Choices.objects.get(id=choiceid)
        choice.votes += 1
        choice.save()

        request.user.questions.add(Question.objects.get(id=qid))
        # 返回当前投票问题的投票结果页
        url = reverse("polls:result", args=(qid,))
        # 投票成功 返回投票结果

        # redirect其实没有真正的返回内容   而是让浏览器重新请求一个地址
        # 不能反复刷新post的结果
        # question = Question.objects.get(id=qid)
        # 错误的结局  刷新页面导致数据出错
        # return render(request,'polls/result.html',{"question":question})
        return redirect(to=url)
        # return HttpResponse("投票成功了")  #接受了详情页的post请求
        # return HttpResponse("现在我代替你进入到了投票结果页")  # 接受了结果页的get请求

        # except:
        #     return HttpResponse("选项不合法")
    # return HttpResponse("详情页"+qid)


class DetailView(View):
    def get(self, request, qid):
        try:
            question = Question.objects.get(id=qid)
            print(question, "--")
            # 使用render发起一起请求
            return render(request, 'polls/detail.html', {"question": question})

        except Exception as e:
            print(e)
            return HttpResponse("问题不合法")

    def post(self, request, qid):
        choiceid = request.POST.get("num")
        try:
            choice = Choices.objects.get(id=choiceid)
            choice.votes += 1
            choice.save()
            # 返回当前投票问题的投票结果页
            url = reverse("polls:result", args=(qid,))
            # 投票成功 返回投票结果

            # redirect其实没有真正的返回内容   而是让浏览器重新请求一个地址
            # 不能反复刷新post的结果
            # question = Question.objects.get(id=qid)
            # 错误的结局  刷新页面导致数据出错
            # return render(request,'polls/result.html',{"question":question})
            return redirect(to=url)
            # return HttpResponse("投票成功了")  #接受了详情页的post请求
            # return HttpResponse("现在我代替你进入到了投票结果页")  # 接受了结果页的get请求

        except Exception as e:
            print(e)
            return HttpResponse("选项不合法")


def result(request, qid):
    try:
        question = Question.objects.get(id=qid)
        return render(request, 'polls/result.html', {"question": question})
    except Exception as e:
        print(e)
        return HttpResponse("问题不合法")


class ResultView(View):
    # 方法一 继承View
    def get(self, request, qid):
        try:
            question = Question.objects.get(id=qid)
            return render(request, 'polls/result.html', {"question": question})
        except Exception as e:
            print(e)
            return HttpResponse("问题不合法")


def login(request):
    if request.method == "GET":
        lf = LoginFrom()
        return render(request, 'polls/login.html', {'lf': lf})
    elif request.method == "POST":
        lf = LoginFrom(request.POST)
        if lf.is_valid():
            username = lf.cleaned_data['username']
            password = lf.cleaned_data['password']
            # username = request.POST.get("username")
            # password = request.POST.get("password")
            # 可以使用django自带的用户认证系统  认证成功返回用户 失败返回None
            user = authenticate(username=username, password=password)
            # 调用django登录方法  其实是为了生成cookie
            if user:
                lin(request, user)
                next = request.GET.get("next")
                print("取得next参数为", next)
                if next:
                    url = next
                else:
                    url = reverse("polls:index")
                return redirect(to=url)
            else:
                # url = reverse("polls:login")
                # return redirect(to=url)
                lf = LoginFrom()
                return render(request, 'polls/login.html', {'errors': '用户名或者密码错误', 'lf': lf})

        else:
            return HttpResponse('未知错误')


def regist(request):
    if request.method == "GET":
        rf = RegistFrom()
        return render(request, 'polls/regist.html', {'rf': rf})
    else:
        rf = RegistFrom(request.POST)
        if rf.is_valid():
            username = rf.cleaned_data["username"]
            password = rf.cleaned_data["password"]
            password2 = rf.cleaned_data["password2"]
            if User.objects.filter(username=username).count() > 0:
                rf = RegistFrom()
                return render(request, 'polls/regist.html', {'errors': '用户名已存在', 'rf': rf})
            else:
                if password == password2:
                    rf.save()
                    # User.objects.create_user(username=username, password=password)
                    url = reverse("polls:login")
                    return redirect(to=url)
                else:
                    rf = RegistFrom()
                    return render(request, 'polls/regist.html', {'errors': '俩次输入的密码不一致', 'rf': rf})


def logout(request):
    # 调用django的登出方法 目的是为了删除cookie
    lot(request)
    url = reverse("polls:index")
    return redirect(to=url)
