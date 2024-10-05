# myapp/urls.py

from django.urls import path
from . import views
from .views import get_produit_data
urlpatterns = [
    path('', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),  # Define the logout URL
   ####################################################
    path('page_facture/', views.facturation_page, name='page_facture'),# URL for Nouvelle Facture
    path('facture/', views.facturation_page, name='facturation_page'),
    path('get_produit_data/', get_produit_data, name='get_produit_data'),
    path('factureN/', views.factureN, name='factureN'),
    path('facturation/', views.facturation_page, name='facturation_page'),
    path('save_facturation/', views.save_facturation, name='save_facturation'),
    path('save_clients/', views.save_clients, name='save_clients'),
    path('get_produit_data/', views.get_produit_data, name='get_produit_data'),
    path('facturation/', views.facturation_page, name='facturation_page'),
    path('ajouter_facturation/', views.ajouter_facturation, name='ajouter_facturation'),
    path('modifier_facturation/<int:facturation_id>/', views.modifier_facturation, name='modifier_facturation'),
    path('supprimer_facturation/<int:facturation_id>/', views.supprimer_facturation, name='supprimer_facturation'),
   ####################################################
    path('page_bon_livraison/', views.page_bon_livraison, name='page_bon_livraison'),  # URL for Nouvelle Bon de Sortie
    path('products/', views.manage_products, name='manage_products'),  # URL for Products page
   #################################
    path('products/edit/<int:pk>/', views.edit_produit, name='edit_produit'),
    path('products/delete/<int:pk>/', views.delete_produit, name='delete_produit'),
    
   ##################################################################
   # URL for Clients page
    path('clients/', views.manage_clients, name='manage_clients'),
    path('clients/edit/<int:pk>/', views.edit_client, name='edit_client'),
    path('clients/delete/<int:pk>/', views.delete_client, name='delete_client'),
  
  ########################################################################################
    path('invoice-history/', views.invoice_history, name='historique_factures'),  # URL for Invoice History page
    #path('select_client/', views.select_client, name='select_client'),
    #path('historique_factures/<int:client_id>/', views.historique_factures, name='historique_factures'),
   #path('voir-facture/<int:facture_id>/', views.voir_facture, name='voir_facture'),
   #path('supprimer-facture/<int:facture_id>/', views.supprimer_facture, name='supprimer_facture'),
   #path('generer-facture/<int:client_id>/', views.generer_facture, name='generer_facture'),
  ##############################################################################
    path('bl-history/', views.bl_history, name='bl_history'),  # URL for BL History page # Add other URL patterns as needed

]
