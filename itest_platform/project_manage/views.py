from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required


def hello(request):
    if request.method == "GET":
        name = request.GET.get("name", "")
        print(name)
        return render(request, "hello.html", {"name": name})


def index(request):
    """
    返回index页面
    """
    if request.method == "GET":
        return render(request, "index.html")

    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")

        if username == "" or password == "":
            return render(request, "index.html", {"error": "can't be null"})

        user = auth.authenticate(username=username, password=password)
        print("user:", user)

        if user is not None:
            auth.login(request, user)  # 到数据库写session key
            return HttpResponseRedirect("/manage/")
        else:
            return render(request, "index.html", {"error": "wrong "})


@login_required
def manage(request):
    return render(request, "manage.html")


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/index/")
