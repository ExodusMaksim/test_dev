from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from app_manage.models import Project
from app_manage.forms import ProjectForm


@login_required
def manage(request):
    project = Project.objects.all()
    username = request.session.get("user", "")
    return render(request, "navigation.html", {"user": username, "project": project})


@login_required
def project_add(request):
    """
    项目添加
    """
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            describe = form.cleaned_data['describe']
            status = form.cleaned_data['status']
            Project.objects.create(name=name, describe=describe, status=status)
            return HttpResponseRedirect('/project/')
    else:
        form = ProjectForm()
        username = request.session.get('user', '')
        return render(request, "project/add.html", {"user": username, "form": form})


@login_required
def project_edit(request, pid):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = Project.objects.get(id=pid)
            project.name = form.cleaned_data['name']
            project.describe = form.cleaned_data['describe']
            project.status = form.cleaned_data['status']
            project.save()
            return HttpResponseRedirect('/project/')
    else:
        if pid:
            try:
                p = Project.objects.get(id=pid)
                form = ProjectForm(instance=p)
                return render(request, "project/edit.html", {"form": form, "pid": pid})
            except Project.DoesNotExist:
                return HttpResponseRedirect('/project/')


@login_required
def project_delete(request, pid):
    try:
        p = Project.objects.get(id=pid)
        p.delete()
    except Project.DoesNotExist:
        return HttpResponseRedirect('/project/')
    else:
        return HttpResponseRedirect('/project/')
