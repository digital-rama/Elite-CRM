from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User, Group
from manpower.models import *
from project.models import *
from django.contrib import messages
from manpower.forms import *
from django.contrib.auth.decorators import login_required
from manpower.decoraters import *
from django.forms import modelformset_factory


# from .server import check_servers

# Create your views here.


# Error 404 & 500 Handeler - Start

def error_404_views(request, exception):
    return render(request, 'manpower/404.html')


def error_500_views(request):
    return render(request, 'manpower/404.html')

# Error 404 & 500 Handeler - End


def uaaccess(request):
    name = request.user.first_name
    context = {'name': name}
    return render(request, 'manpower/uaaccess.html', context)


@admin_only
def dashboard(request):

    context = {}
    return render(request, 'manpower/dashboard.html', context)


@allowed_users(allowed_roles=['supervisor'])
def super_dashboard(request):
    context = {}
    return render(request, 'manpower/super_dashboard.html', context)


@allowed_users(allowed_roles=['master', 'admin'])
def tenders(request):
    tender_list = Tender.objects.all()
    context = {'tender_list': tender_list}
    return render(request, 'manpower/tenders.html', context)


@allowed_users(allowed_roles=['master', 'admin'])
def add_tender(request):
    if request.method == 'POST':
        form = addTender(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/tenders/')
    else:
        form = addTender()
    return render(request, 'manpower/add_tender.html', {'form': form})


@allowed_users(allowed_roles=['master', 'admin'])
def tender_details(request, id):
    tender_object = Tender.objects.get(id=id)
    other_contractor = otherContractors.objects.filter(tender=tender_object)
    oclen = len(other_contractor)
    project_obj = Projects.objects.filter(tender=tender_object)
    polen = len(project_obj)

    context = {'tender_object': tender_object,
               'other_contractor': other_contractor, 'project_obj': project_obj, 'oclen': oclen, 'polen': polen}
    return render(request, 'manpower/tender_details.html', context)


@allowed_users(allowed_roles=['master', 'admin'])
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


@allowed_users(allowed_roles=['master', 'admin'])
def detete_tender(request, id):
    obj = Tender.objects.get(id=id)
    if request.method == 'POST':
        obj.delete()
        return redirect('/tenders/')

    context = {'obj': obj}
    return render(request, 'manpower/delete_tender.html', context)


def projects(request):
    if request.user.is_staff:
        all_projects = Projects.objects.all()
        projlen = len(all_projects)
    else:
        usern = request.user.username
        super_id = SuperVisors.objects.get(username=usern)
        all_projects = Projects.objects.filter(superviser=super_id)
        projlen = len(all_projects)

    context = {'all_projects': all_projects, 'projlen': projlen}
    return render(request, 'manpower/projects.html', context)


@allowed_users(allowed_roles=['master', 'admin'])
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


@allowed_users(allowed_roles=['master', 'admin'])
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


@allowed_users(allowed_roles=['master', 'admin'])
def delete_contractor(request, id):
    obj = otherContractors.objects.get(id=id)
    obj.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@allowed_users(allowed_roles=['master', 'admin'])
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


@allowed_users(allowed_roles=['master', 'admin'])
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


@allowed_users(allowed_roles=['master', 'admin'])
def delete_project(request, id, tid):
    obj = Projects.objects.get(id=id)
    tender_obj = Tender.objects.get(id=tid)
    if request.method == 'POST':
        obj.delete()
        return redirect('/tender_details/' + str(Tender.objects.get(id=tid).id))

    context = {'obj': obj, 'tender_obj': tender_obj, }
    return render(request, 'manpower/delete_project.html', context)


def project_details(request, id):
    project_obj = Projects.objects.get(id=id)
    project_start_obj = ProjectStart.objects.filter(project=project_obj)
    security_deposit_obj = Security_Deposit.objects.filter(project=project_obj)
    project_repeter = ProjectRepeter.objects.all()
    labour_obj = labour.objects.filter(project=project_obj)
    prlen = len(project_repeter)
    lablen = len(labour_obj)
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
               'esd': esd, 'sp': sp, 'project_repeter': project_repeter, 'prlen': prlen,
               'labour_obj': labour_obj, 'lablen': lablen,
               }
    return render(request, 'manpower/project_details.html', context)


@allowed_users(allowed_roles=['master', 'admin'])
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


@allowed_users(allowed_roles=['master', 'admin'])
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


@allowed_users(allowed_roles=['master', 'admin'])
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


@allowed_users(allowed_roles=['master', 'admin'])
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


@allowed_users(allowed_roles=['master', 'admin'])
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


@allowed_users(allowed_roles=['master', 'admin'])
def edit_pr(request, id, pid):
    edit_Project_repeter = ProjectRepeter.objects.get(id=id)
    if request.method == 'POST':
        form = projectRep(request.POST,  request.FILES,
                          instance=edit_Project_repeter)
        if form.is_valid():
            form.save()

            return redirect('/project_details/' + str(Projects.objects.get(id=pid).id))
    else:
        form = projectRep(instance=edit_Project_repeter)

    context = {'form': form}
    return render(request, 'manpower/edit_pr.html', context)


@allowed_users(allowed_roles=['master', 'admin'])
def delete_pr(request, id, pid):
    pr_obj = ProjectRepeter.objects.get(id=id)
    project_obj = Projects.objects.get(id=pid)
    if request.method == 'POST':
        pr_obj.delete()
        return redirect('/project_details/' + str(Projects.objects.get(id=pid).id))

    context = {'pr_obj': pr_obj, 'project_obj': project_obj}
    return render(request, 'manpower/delete_pr.html', context)


def create_followup(request, id, pid):
    if request.method == 'POST':
        form = projectFollow(request.POST)
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.project_rep = ProjectRepeter.objects.get(id=id)
            form_data.save()
            return redirect('/project_details/' + str(Projects.objects.get(id=pid).id))
    else:
        form = projectFollow()

    context = {'form': form, }
    return render(request, 'manpower/create_followup.html', context)


def view_followup(request, id, pid):
    pr_obj = ProjectRepeter.objects.get(id=id)
    view_follow = ProjectFollowup.objects.filter(project_rep=pr_obj)
    project_obj = Projects.objects.get(id=pid)

    context = {'view_follow': view_follow, 'project_obj': project_obj}
    return render(request, 'manpower/view_followup.html', context)


# Supervisor & Labour Views
# Supervisor & Labour Views
# Supervisor & Labour Views


@allowed_users(allowed_roles=['master', 'admin'])
def supervisors(request):
    super_count = len(SuperVisors.objects.all())
    all_super = SuperVisors.objects.all()
    context = {'all_super': all_super, 'super_count': super_count}
    return render(request, 'manpower/supervisors.html', context)


@allowed_users(allowed_roles=['master', 'admin'])
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
                group = Group.objects.get(name='supervisor')
                user.groups.add(group)
                return redirect('/supervisors/')
            else:
                messages.error(
                    request, "Password & Confirm Password Doesn't Match")
    else:
        form = SupervisorForm()

    context = {'form': form}
    return render(request, 'manpower/create_supervisor.html', context)


@allowed_users(allowed_roles=['master', 'admin'])
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


@allowed_users(allowed_roles=['master', 'admin'])
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


@allowed_users(allowed_roles=['master', 'admin'])
def laboursnd(request):
    labour_skill = labourSkillType.objects.all()
    labour_desig = labourDesignation.objects.all()

    context = {'labour_skill': labour_skill, 'labour_desig': labour_desig}
    return render(request, 'manpower/laboursnd.html', context)


@allowed_users(allowed_roles=['master', 'admin'])
def addlabdeg(request):
    if request.method == 'POST':
        form = labourDesig(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/laboursnd/')
    else:
        form = labourDesig()

    context = {'form': form}
    return render(request, 'manpower/addlabdeg.html', context)


@allowed_users(allowed_roles=['master', 'admin'])
def addlabskill(request):
    if request.method == 'POST':
        form = labourSkill(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/laboursnd/')
    else:
        form = labourSkill()

    context = {'form': form}
    return render(request, 'manpower/addlabskill.html', context)


@allowed_users(allowed_roles=['master', 'admin'])
def delete_labskill(request, id):
    obj = labourSkillType.objects.get(id=id)
    obj.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@allowed_users(allowed_roles=['master', 'admin'])
def delete_labdeg(request, id):
    obj = labourDesignation.objects.get(id=id)
    obj.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def addlabour(request, id):
    if request.method == 'POST':
        form = addLabour(request.POST, request.FILES)
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.project = Projects.objects.get(id=id)
            form_data.save()
            return redirect('/project_details/' + str(Projects.objects.get(id=id).id))
    else:
        form = addLabour()

    context = {'form': form}
    return render(request, 'manpower/add_project.html', context)


@allowed_users(allowed_roles=['master', 'admin'])
def edit_Labour(request, id, pid):
    editlabour = labour.objects.get(id=id)
    form = addLabour(instance=editlabour)
    if request.method == 'POST':
        form = addLabour(request.POST, request.FILES, instance=editlabour)
        if form.is_valid():
            form.save()
            return redirect('/project_details/' + str(Projects.objects.get(id=pid).id))

        else:
            form = addLabour(instance=editlabour)

    context = {'form': form}
    return render(request, 'manpower/add_project.html', context)


@allowed_users(allowed_roles=['master', 'admin'])
def delete_labour(request, id, pid):
    obj = labour.objects.get(id=id)
    project_obj = Projects.objects.get(id=pid)
    if request.method == 'POST':
        obj.delete()
        return redirect('/project_details/' + str(Projects.objects.get(id=pid).id))

    context = {'obj': obj, 'project_obj': project_obj}
    return render(request, 'manpower/delete_labour.html', context)


@allowed_users(allowed_roles=['master', 'admin'])
def all_labours(request):
    all_labours = labour.objects.all()

    context = {'all_labours': all_labours}
    return render(request, 'manpower/all_labours.html', context)


def labour_attendance(request, id, pid):
    labour_obj = labour.objects.get(id=id)
    labour_attendance_obj = Attendance.objects.filter(labour=labour_obj)
    if request.method == 'POST':
        form = labourAttendance(request.POST)
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.project = Projects.objects.get(id=pid)
            form_data.labour = labour.objects.get(id=id)
            form_data.save()
            if request.POST.get('Save'):
                return redirect('/project_details/' + str(Projects.objects.get(id=pid).id))
            if request.POST.get('NewForm'):
                return redirect(labour_attendance, id=id, pid=pid)

    else:
        form = labourAttendance()

    context = {'form': form, 'labour_obj': labour_obj,
               'labour_attendance_obj': labour_attendance_obj}
    return render(request, 'manpower/attendance.html', context)


def all_attendance(request, id):
    project_obj = Projects.objects.get(id=id)
    attendance = Attendance.objects.filter(project=project_obj)
    labour_count = len(labour.objects.filter(project=project_obj))

    context = {'attendance': attendance,
               'project_obj': project_obj, 'labour_count': labour_count}
    return render(request, 'manpower/all_attendance.html', context)
