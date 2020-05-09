from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from manpower.models import *
from project.models import *
from django.contrib import messages
from manpower.forms import *
from django.contrib.auth.decorators import login_required


# from .server import check_servers

# Create your views here.


# Error 404 & 500 Handeler - Start

def handler404(request, exception):
    return render(request, 'manpower/404.html')


def handler500(request):
    return render(request, 'manpower/404.html')

# Error 404 & 500 Handeler - End


@login_required
def dashboard(request):

    context = {}
    return render(request, 'manpower/dashboard.html', context)


@login_required
def tenders(request):
    tender_list = Tender.objects.all()
    context = {'tender_list': tender_list}
    return render(request, 'manpower/tenders.html', context)


@login_required
def add_tender(request):
    if request.method == 'POST':
        form = addTender(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/tenders/')
    else:
        form = addTender()
    return render(request, 'manpower/add_tender.html', {'form': form})


@login_required
def tender_details(request, id):
    tender_object = Tender.objects.get(id=id)
    other_contractor = otherContractors.objects.filter(tender=tender_object)
    oclen = len(other_contractor)
    project_obj = Projects.objects.filter(tender=tender_object)
    polen = len(project_obj)

    context = {'tender_object': tender_object,
               'other_contractor': other_contractor, 'project_obj': project_obj, 'oclen': oclen, 'polen': polen}
    return render(request, 'manpower/tender_details.html', context)


@login_required
def edit_tender(request, id):
    editTender = Tender.objects.get(id=id)
    form = addTender(instance=editTender)
    if request.method == 'POST':
        form = addTender(request.POST, request.FILES, instance=editTender)
        if form.is_valid():
            form.save()
            return redirect('/tenders/')
    else:
        form = addTender(instance=editTender)

    context = {'form': form}
    return render(request, 'manpower/add_tender.html', context)


@login_required
def detete_tender(request, id):
    obj = Tender.objects.get(id=id)
    if request.method == 'POST':
        obj.delete()
        return redirect('/tenders/')

    context = {'obj': obj}
    return render(request, 'manpower/delete_tender.html', context)


@login_required
def projects(request):

    all_projects = Projects.objects.all()
    context = {'all_projects': all_projects}
    return render(request, 'manpower/projects.html', context)


@login_required
def add_contractor(request, id):
    tender = Tender.objects.get(id=id)
    if request.method == 'POST':
        form = otherContractorsForm(request.POST)
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.tender = Tender.objects.get(id=id)
            form_data.save()
            if request.POST.get('Save'):
                return redirect('/tender_details/'+str(Tender.objects.get(id=id).id))
            if request.POST.get('NewForm'):
                return redirect('/add_contractor/'+str(id))
    else:
        form = otherContractorsForm()

    context = {'form': form, 'tender': tender}
    return render(request, 'manpower/add_contractor.html', context)


@login_required
def edit_contractor(request, id, tid):
    editContractor = otherContractors.objects.get(id=id)
    form = otherContractorsForm(instance=editContractor)
    if request.method == 'POST':
        form = otherContractorsForm(request.POST, instance=editContractor)
        if form.is_valid():
            form.save()
            return redirect('/tender_details/' + str(Tender.objects.get(id=tid).id))

        else:
            form = otherContractorsForm(instance=editContractor)

    context = {'form': form}
    return render(request, 'manpower/edit_contractor.html', context)


@login_required
def delete_contractor(request, id):
    obj = otherContractors.objects.get(id=id)
    obj.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def add_project(request, id):
    if request.method == 'POST':
        form = addProject(request.POST)
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.tender = Tender.objects.get(id=id)
            form_data.save()
            return redirect('/tender_details/' + str(Tender.objects.get(id=id).id))
    else:
        form = addProject()

    context = {'form': form}
    return render(request, 'manpower/add_project.html', context)


@login_required
def edit_project(request, id, tid):
    editProject = Projects.objects.get(id=id)
    form = addProject(instance=editProject)
    if request.method == 'POST':
        form = addProject(request.POST, instance=editProject)
        if form.is_valid():
            form.save()
            return redirect('/tender_details/' + str(Tender.objects.get(id=tid).id))

        else:
            form = addProject(instance=editProject)

    context = {'form': form}
    return render(request, 'manpower/add_project.html', context)


@login_required
def delete_project(request, id, tid):
    obj = Projects.objects.get(id=id)
    tender_obj = Tender.objects.get(id=tid)
    project_start_len = len(ProjectStart.objects.filter(project=obj))
    security_deposit_len = len(Security_Deposit.objects.filter(project=obj))
    if request.method == 'POST':
        obj.delete()
        return redirect('/tender_details/' + str(Tender.objects.get(id=tid).id))

    context = {'obj': obj, 'tender_obj': tender_obj,
               'project_start_len': project_start_len, 'security_deposit_len': security_deposit_len}
    return render(request, 'manpower/delete_project.html', context)


@login_required
def project_details(request, id):
    project_obj = Projects.objects.get(id=id)
    project_start_obj = ProjectStart.objects.filter(project=project_obj)
    security_deposit_obj = Security_Deposit.objects.filter(project=project_obj)
    project_repeter = ProjectRepeter.objects.all()
    prlen = len(project_repeter)
    # Submit & Edit Project Show & hide
    if len(project_start_obj) >= 1:
        sp = 'hide'
    else:
        sp = Projects.objects.get(id=id)

    if len(project_start_obj) < 1:
        ep = 'hide'
    else:
        ep = Projects.objects.get(id=id)

    # Security Dposit Buttons Show & Hide
    if len(security_deposit_obj) >= 1:
        asd = 'hide'
    else:
        asd = Projects.objects.get(id=id)

    if len(security_deposit_obj) < 1:
        esd = 'hide'
    else:
        esd = Projects.objects.get(id=id)

    context = {'project_obj': project_obj,
               'project_start_obj': project_start_obj, 'ep': ep,
               'security_deposit_obj': security_deposit_obj, 'asd': asd,
               'esd': esd, 'sp': sp, 'project_repeter': project_repeter, 'prlen': prlen}
    return render(request, 'manpower/project_details.html', context)


def add_project_start(request, id):
    if request.method == 'POST':
        form = addProjectStart(request.POST,  request.FILES)
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.project = Projects.objects.get(id=id)
            form_data.save()
            return redirect('/project_details/' + str(Projects.objects.get(id=id).id))
    else:
        form = addProjectStart()

    context = {'form': form}
    return render(request, 'manpower/add_project_start.html', context)


@login_required
def edit_project_start(request, id, pid):
    editStartProject = ProjectStart.objects.get(id=id)
    form = addProjectStart(instance=editStartProject)
    if request.method == 'POST':
        form = addProjectStart(request.POST, request.FILES,
                               instance=editStartProject)
        if form.is_valid():
            form.save()
            return redirect('/project_details/' + str(Projects.objects.get(id=pid).id))

        else:
            form = addProjectStart(instance=editStartProject)

    context = {'form': form}
    return render(request, 'manpower/add_project_start.html', context)


def security_deposit(request, id):
    if request.method == 'POST':
        form = securityDeposit(request.POST,  request.FILES)
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.project = Projects.objects.get(id=id)
            form_data.save()
            return redirect('/project_details/' + str(Projects.objects.get(id=id).id))
    else:
        form = securityDeposit()

    context = {'form': form}
    return render(request, 'manpower/security_deposit.html', context)


@login_required
def edit_security_deposit(request, id):
    editSecurityDeposit = Security_Deposit.objects.get(id=id)
    form = securityDeposit(instance=editSecurityDeposit)
    if request.method == 'POST':
        form = securityDeposit(request.POST, request.FILES,
                               instance=editSecurityDeposit)
        if form.is_valid():
            form.save()
            return redirect('/project_details/' + str(Projects.objects.get(id=id).id))

        else:
            form = securityDeposit(instance=editSecurityDeposit)

    context = {'form': form}
    return render(request, 'manpower/security_deposit.html', context)


def project_repeter(request, id):
    if request.method == 'POST':
        form = projectRep(request.POST,  request.FILES)
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.project = Projects.objects.get(id=id)
            form_data.save()
            return redirect('/project_details/' + str(Projects.objects.get(id=id).id))
    else:
        form = projectRep()

    context = {'form': form}
    return render(request, 'manpower/project_repeter.html', context)


def create_followup(request, id):
    if request.method == 'POST':
        form = projectFollow(request.POST)
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.project_rep = ProjectRepeter.objects.get(id=id)
            form_data.save()
            return redirect('/project_details/' + str(Projects.objects.get(id=id).id))
    else:
        form = projectFollow()

    context = {'form': form}
    return render(request, 'manpower/create_followup.html', context)


# Supervisor & Labour Views
# Supervisor & Labour Views
# Supervisor & Labour Views


@login_required
def supervisors(request):
    super_count = len(SuperVisors.objects.all())
    all_super = SuperVisors.objects.all()
    context = {'all_super': all_super, 'super_count': super_count}
    return render(request, 'manpower/supervisors.html', context)


@login_required
def create_supervisor(request):
    if request.method == 'POST':
        form = SupervisorForm(request.POST, request.FILES)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            re_password = request.POST.get('re_password')
            email = request.POST.get('email')
            splitname = request.POST.get('name').split()

            if password == re_password:
                user = User.objects.create_user(username, email, password)
                user.first_name = splitname[0]
                user.last_name = splitname[1]
                user.save()
                form.save()
                return redirect('/supervisors/')
            else:
                messages.error(
                    request, "Password & Confirm Password Doesn't Match")
    else:
        form = SupervisorForm()

    context = {'form': form}
    return render(request, 'manpower/create_supervisor.html', context)


@login_required
def edit_supervisor(request, id):
    editSupervisor = SuperVisors.objects.get(id=id)
    form = SupervisorForm(instance=editSupervisor)
    if request.method == 'POST':
        form = SupervisorForm(request.POST, request.FILES,
                              instance=editSupervisor)
        if form.is_valid():
            form.save()
            return redirect('/supervisors/')
    else:
        form = SupervisorForm(instance=editSupervisor)

    context = {'form': form}
    return render(request, 'manpower/create_supervisor.html', context)


@login_required
def detete_supervisor(request, id):
    obj = SuperVisors.objects.get(id=id)
    username = obj.username
    user = User.objects.get(username=username)
    if request.method == 'POST':
        obj.delete()
        user.delete()
        return redirect('/supervisors/')

    context = {'obj': obj}
    return render(request, 'manpower/delete_Supervisor.html', context)
