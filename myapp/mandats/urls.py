from django.conf.urls import url
from django.urls import path
from . import views
from django.views.generic import TemplateView

from .views import ContactFoundation
from django.contrib.auth import views as auth_views

urlpatterns = [
    # url(r'^home/$', views.home, name='home'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^profile/$', views.view_profile, name='view_profile'),
    url(r'^profile/(?P<pk>\d+)/$', views.view_profile, name='view_profile_with_pk'),
    url(r'^profile/edit/$', views.edit_profile, name='edit_profile'),
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'^activation_complete/$', views.activation_complete, name='activation_complete'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]

urlpatterns += [
    path('', views.index, name='index'),
    path('mandats/', views.MandatListView.as_view(), name='mandats'),
    path('mandat/<str:pk>', views.MandatDetailView.as_view(), name='mandat-detail'),
    path('fournisseurs/', views.FournisseurListView.as_view(), name='fournisseurs'),
    path('fournisseur/<str:pk>', views.FournisseurDetailView.as_view(), name='fournisseur-detail'),
    path('virements/', views.VirementListView.as_view(), name='virements'),
    path('virement/<str:pk>', views.VirementDetailView.as_view(), name='virement-detail'),
]
urlpatterns += [
    path('mesmandats/', views.LoanedMandatByUserListView.as_view(), name='mandat-utilisateur'),
    path('mesvirements/', views.LoanedVirementByUserListView.as_view(), name='virement-utilisateur'),
]

urlpatterns += [
    path('fondation/', ContactFoundation.as_view(), name='contact_foundation'),
    path('sent/', TemplateView.as_view(template_name='mandats/sent.html'), name='contact_form_sent'),
]