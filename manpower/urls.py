from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('uaaccess/', views.uaaccess, name='uaaccess'),
    path('tenders/', views.tenders, name='tenders'),
    path('super_dashboard/', views.super_dashboard, name='super_dashboard'),
    path('add_tender/', views.add_tender, name='add_tender'),
    path('edit_tender/<int:id>/', views.edit_tender, name='edit_tender'),
    path('detete_tender/<int:id>/', views.detete_tender, name='delete_tender'),
    path('tender_details/<int:id>/', views.tender_details, name='tender_details'),
    path('add_contractor/<int:id>/', views.add_contractor, name='add_contractor'),
    path('edit_contractor/<int:id>/<int:tid>/',
         views.edit_contractor, name='edit_contractor'),
    path('delete_contractor/<int:id>/',
         views.delete_contractor, name='delete_contractor'),
    path('edit_project/<int:id>/<int:tid>/',
         views.edit_project, name='edit_project'),
    path('projects/', views.projects, name='projects'),
    path('add_project/<int:id>', views.add_project, name='add_project'),
    path('delete_project/<int:id>/<int:tid>/',
         views.delete_project, name='delete_project'),
    path('project_details/<int:id>', views.project_details, name='project_details'),
    path('add_project_start/<int:id>',
         views.add_project_start, name='add_project_start'),
    path('edit_project_start/<int:id>/<int:pid>/',
         views.edit_project_start, name='edit_project_start'),
    path('security_deposit/<int:id>',
         views.security_deposit, name='security_deposit'),
    path('edit_security_deposit/<int:id>',
         views.edit_security_deposit, name='edit_security_deposit'),
    path('project_repeter/<int:id>', views.project_repeter, name='project_repeter'),
    path('edit_pr/<int:id>/<int:pid>', views.edit_pr, name='edit_pr'),
    path('delete_pr/<int:id>/<int:pid>', views.delete_pr, name='delete_pr'),
    path('create_followup/<int:id>/<int:pid>',
         views.create_followup, name='create_followup'),
    path('view_followup/<int:id>/<int:pid>',
         views.view_followup, name='view_followup'),
    path('create_supervisor/', views.create_supervisor, name='create_supervisor'),
    path('edit_supervisor/<int:id>', views.edit_supervisor, name='edit_supervisor'),
    path('detete_supervisor/<int:id>',
         views.detete_supervisor, name='detete_supervisor'),
    path('supervisors/', views.supervisors, name='supervisors'),
    path('laboursnd/', views.laboursnd, name='laboursnd'),
    path('addlabdeg/', views.addlabdeg, name='addlabdeg'),
    path('addlabskill/', views.addlabskill, name='addlabskill'),
    path('delete_labskill/<int:id>', views.delete_labskill, name='delete_labskill'),
    path('delete_labdeg/<int:id>', views.delete_labdeg, name='delete_labdeg'),
    path('addlabour/<int:id>', views.addlabour, name='addlabour'),
    path('edit_Labour/<int:id>/<int:pid>',
         views.edit_Labour, name='edit_Labour'),
    path('delete_labour/<int:id>/<int:pid>',
         views.delete_labour, name='delete_labour'),
    path('labour_attendance/<int:id>/<int:pid>',
         views.labour_attendance, name='labour_attendance'),
    path('all_labours/', views.all_labours, name='all_labours'),
    path('all_attendance/<int:id>', views.all_attendance, name='all_attendance'),
    path('login/', auth_views.LoginView.as_view(template_name='manpower/login.html'), name='login'),
    path('logoutuser/', auth_views.LogoutView.as_view(
        next_page=settings.LOGOUT_REDIRECT_URL), name='logoutuser'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
