from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from app_manage.models import Project, Module
from app_manage.forms import ProjectForm, ModuleForm


@login_required
def module(request):
    modules = Module.objects.all()
    print(modules)
    username = request.session.get("user", "")
    return render(request, "module/module.html", {"user": username, "modules": modules})


@login_required
def module_add(request):
    """
    添加模块
    """
    if request.method == "POST":
        form = ModuleForm(request.POST)
        if form.is_valid():
            project = form.cleaned_data['project']
            name = form.cleaned_data['name']
            describe = form.cleaned_data['describe']
            Module.objects.create(project=project, name=name, describe=describe)
            return HttpResponseRedirect('/module/')
    else:
        modules = ModuleForm()
        username = request.session.get('user', '')
        return render(request, "module/add.html", {"user": username, "modules": modules})


@login_required
def module_edit(request, mid):
    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            module = Module.objects.get(id=mid)
            module.project = form.cleaned_data['project']
            module.name = form.cleaned_data['name']
            module.describe = form.cleaned_data['describe']
            module.save()
            return HttpResponseRedirect('/module/')
    else:
        if mid:
            try:
                m = Project.objects.get(id=mid)
                form = ModuleForm(instance=m)
                username = request.session.get('user', '')
                return render(request, "module/edit.html", {"user": username, "form": form, "mid": mid})
            except Project.DoesNotExist:
                return HttpResponseRedirect('/module/')


@login_required
def module_delete(request, mid):
    try:
        m = Module.objects.get(id=mid)
        m.delete()
    except Project.DoesNotExist:
        return HttpResponseRedirect('/module/')
    else:
        return HttpResponseRedirect('/module/')
