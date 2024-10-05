from django.urls import path
from . import views
from .views import update_article


urlpatterns = [ 
    path('', views.HomeView.as_view(), name='home'),
    
    path('', views.index, name='index'),
    path('delete-invoice/', views.delete_invoice, name='delete-invoice'),
    path('modify-invoice/', views.modify_invoice, name='modify-invoice'),
    path('delete-customer/<int:pk>', views.DeleteCustomerView.as_view() , name='delete_customer'),
    path('edit_customer/<int:pk>/', views.EditCustomerView.as_view(), name='edit_customer'),
    path('add-customer/',views.AddCustomerView.as_view(), name='add-customer'),
    path('add-invoice', views.AddInvoiceView.as_view(), name='add-invoice'),
    path('add-invoice2', views.AddInvoice2View.as_view(), name='add-invoice2'),
    path('view-invoice/<int:pk>', views.InvoiceVisualizationView.as_view(), name='view-invoice'),
    path('view-invoice2/<int:pk>', views.Invoice2VisualizationView.as_view(), name='view-invoice2'),
    path('invoice-pdf/<int:pk>', views.get_invoice_pdf, name="invoice-pdf"),
    path('invoice2-pdf/<int:pk>', views.get_invoice2_pdf, name="invoice2-pdf"),
    
    
    path('delete-article/<int:article_id>/', views.delete_article.as_view(), name='delete-article'),
    
    path('add-invoice3', views.AddInvoice3View.as_view(), name='add-invoice3'),
    path('update-article/<int:article_id>/', update_article, name='update_article'),
    path('delete-produit/<int:article_id>/', views.delete_produit, name='delete_produit'),
]
