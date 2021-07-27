from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    # authentication
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    # poll
    path('', views.index, name='index'),
    path('<int:poll_id>/', views.detail, name='detail'),
    path('<int:poll_id>/vote/', views.vote, name='vote'),
    path('thankyou/', views.thankyou, name='thankyou'),

    # administration
    path('admin/', views.admin, name='admin'),
    path('admin/<int:poll_id>/edit/', views.edit, name='edit'),
    path('admin/<int:poll_id>/results/', views.results, name='results'),
    path('admin/<int:poll_id>/results/summary/', views.summary_results, name='summary_results'),
    path('admin/<int:poll_id>/results/<int:answer_id>/', views.single_result, name='single_result'),

    # action
    path('admin/import/', views.import_poll, name='import_poll'),
    path('admin/<int:poll_id>/export/', views.export_poll, name='export_poll'),
    path('admin/<int:poll_id>/pdf/', views.generate_pdf, name='generate_pdf'),
    path('admin/<int:poll_id>/results/export/', views.export_results, name='export_results')
]
