from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from project_manage.models import Project


@login_required
def manage(request):
    project = Project.objects.all()
    username = request.session.get("user", "")
    return render(request, "manage.html", {"user": username, "project": project})


def project_add(request):
    return render(request, "project/add.html")