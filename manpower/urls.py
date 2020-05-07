from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('tenders/', views.tenders, name='tenders'),
    path('add_tender/', views.add_tender, name='add_tender'),
    path('edit_tender/<int:id>/', views.edit_tender, name='edit_tender'),
    path('detete_tender/<int:id>/', views.detete_tender, name='delete_tender'),
    path('tenders/<slug:uuid_no>/', views.tender_details, name='tender_details'),
    path('add_contractor/<int:id>/', views.add_contractor, name='add_contractor'),
    path('edit_project/<int:id>/<int:tid>/',
         views.edit_project, name='edit_project'),
    path('delete_contractor/<int:id>/',
         views.delete_contractor, name='delete_contractor'),
    path('projects/', views.projects, name='projects'),
    path('add_project/<int:id>', views.add_project, name='add_project'),
    path('edit_contractor/<int:id>/<int:tid>/',
         views.edit_contractor, name='edit_contractor'),
    path('delete_project/<int:id>', views.delete_project, name='delete_project'),
    path('create_supervisor/', views.create_supervisor, name='create_supervisor'),
    path('edit_supervisor/<int:id>', views.edit_supervisor, name='edit_supervisor'),
    path('detete_supervisor/<int:id>',
         views.detete_supervisor, name='detete_supervisor'),
    path('supervisors/', views.supervisors, name='supervisors'),
    path('login/', auth_views.LoginView.as_view(template_name='manpower/login.html'), name='login'),
    path('logoutuser/', auth_views.LogoutView.as_view(
        next_page=settings.LOGOUT_REDIRECT_URL), name='logoutuser'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
