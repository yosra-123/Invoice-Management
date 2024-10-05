from decimal import Decimal
import json
from django.views import View
from .models import * 
import pdfkit
import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from .utils import pagination, get_invoice
from django.urls import reverse_lazy
from django.template.loader import get_template
from django.utils.translation import gettext as _
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.views.generic.edit import UpdateView
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from .models import Article, Invoice
from django.http import JsonResponse
from .forms import ArticleForm
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from decimal import Decimal
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import render

from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Article  # Assuming your model is named `Article`


@csrf_exempt  # Temporarily disable CSRF protection for testing, but handle CSRF later.
def delete_produit(request, article_id):
    if request.method == 'POST':
        article = get_object_or_404(Article, id=article_id)
        article.delete()
        return JsonResponse({'message': 'Produit deleted successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

def article_list(request):
    articles = Article.objects.all()  # Fetch all articles from the database
    paginator = Paginator(articles, 5)  # Show 5 articles per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'add-invoice3.html', {'page_obj': page_obj})


def update_article(request, article_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        # Debugging the incoming data
        print(f"Data received: {data}")
        
        # Extract the data sent from the front end
        code = data.get('code')
        name = data.get('name')
        quantity = data.get('quantity')
        unit_price = data.get('unit_price')
        prix = data.get('prix')

        # Check if any data is missing or invalid
        if not code or not name or not quantity or not unit_price or not prix:
            return JsonResponse({'error': 'Missing or invalid data'}, status=400)
        
        try:
            # Ensure that the quantity and unit_price are numbers
            quantity = float(quantity)
            unit_price = float(unit_price)
            prix = float(prix)
            
            # Perform your update logic here
            article = Article.objects.get(id=article_id)
            article.code = code
            article.name = name
            article.quantity = quantity
            article.unit_price = unit_price
            article.prix = prix
            article.save()

            # Optionally return the updated article data
            return JsonResponse({'message': 'Article updated successfully', 'article': {
                'code': article.code,
                'name': article.name,
                'quantity': article.quantity,
                'unit_price': article.unit_price,
                'prix': article.prix
            }})
        except Exception as e:
            print("Error while updating article:", e)
            return JsonResponse({'error': 'Internal server error'}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

class AddArticleView(View):
    def get(self, request, *args, **kwargs):
        articles = Article.objects.all()
        return render(request, 'add_article.html', {'articles': articles})
    
    def post(self, request, *args, **kwargs):
        code = request.POST.get('code')
        name = request.POST.get('name')
        quantity = request.POST.get('quantity')
        unit_price = request.POST.get('unit_price')
        
        # Check if an article with the same code and name exists
        if Article.objects.filter(code=code, name=name).exists():
            messages.warning(request, 'Un article avec le même code et nom existe déjà.')
        else:
            # Create and save the new article
            Article.objects.create(
                code=code,
                name=name,
                quantity=quantity,
                unit_price=unit_price
            )
            messages.success(request, 'Article ajouté avec succès.')
        
        return redirect('add-article')
    
class DeleteArticleView(LoginRequiredMixin, View):
    def post(self, request, article_id, *args, **kwargs):
        try:
            article = Article.objects.get(id=article_id)
            # Check if the article is linked to any saved invoices or delivery notes
            if Invoice.objects.filter(articles=article).exists():
                messages.error(request, 'Impossible de supprimer cet article car il est lié à des factures enregistrées.')
            else:
                article.delete()
                messages.success(request, 'Article supprimé avec succès.')
        except Article.DoesNotExist:
            messages.error(request, 'Article non trouvé.')
        return redirect('add-invoice3')

class DeleteCustomerView(View):
    def get(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        try:
            customer.delete()
            messages.success(request, 'Le client a été supprimé avec succès.')
        except Exception as e:
            messages.error(request, f'Erreur lors de la suppression du client: {e}')
        return redirect('add-customer')

class EditCustomerView(UpdateView):
    model = Customer
    fields = ['name' , 'phone', 'address', 'city']
    template_name = 'edit_customer.html'
    success_url = reverse_lazy('add-customer')  # Redirect to the add customer page after success

    def form_valid(self, form):
        messages.success(self.request, "Les informations client ont été mises à jour avec succès.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erreur lors de la mise à jour des informations client. Veuillez vérifier le formulaire.")
        return super().form_invalid(form)
    
def delete_invoice(request):
    if request.method == 'POST':
        invoice_id = request.POST.get('invoice_id')
        try:
            invoice = Invoice.objects.get(pk=invoice_id)
            invoice.delete()
            return JsonResponse({'success': True})
        except Invoice.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'La facture n existe pas.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

def modify_invoice(request):
    if request.method == 'POST':
        invoice_id = request.POST.get('invoice_id')
        # Get other modified data from the POST request and update the invoice
        try:
            invoice = Invoice.objects.get(pk=invoice_id)
            # Update invoice fields
            invoice.save()
            return JsonResponse({'success': True})
        except Invoice.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'La facture n existe pas.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


def index(request):
    invoices = Invoice.objects.all()
    return render(request, 'index.html', {'invoices': invoices})

class HomeView(LoginRequiredMixin, View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        invoices = Invoice.objects.select_related('customer', 'save_by').all().order_by('-invoice_date_time')
        items = pagination(request, invoices)
        context = {
            'invoices': items
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if request.POST.get('id_modified'):
            paid = request.POST.get('modified')
            try:
                obj = Invoice.objects.get(id=request.POST.get('id_modified'))
                obj.paid = (paid == 'True')
                obj.save()
                messages.success(request, _("Modification effectuée avec succès."))
            except Exception as e:
                messages.error(request, f"Désolé, l'erreur suivante s'est produite: {e}.")
        
        if request.POST.get('id_supprimer'):
            try:
                obj = Invoice.objects.get(pk=request.POST.get('id_supprimer'))
                obj.delete()
                messages.success(request, _("La suppression a réussi."))
            except Exception as e:
                messages.error(request, f"Désolé, l'erreur suivante s'est produite: {e}.")
        
        invoices = Invoice.objects.select_related('customer', 'save_by').all().order_by('-invoice_date_time')
        items = pagination(request, invoices)
        context = {
            'invoices': items
        }
        return render(request, self.template_name, context)
  

from django.db.models import Q

class AddCustomerView(LoginRequiredMixin, View):
    def get(self, request):
        customers = Customer.objects.all()
        return render(request, 'add_customer.html', {'customers': customers})
    
    def post(self, request):
        name = request.POST['name']
       
        phone = request.POST['phone']
        address = request.POST['address']
        city = request.POST['city']
        save_by = request.user
        
        # Check if a customer with the same details already exists
        if Customer.objects.filter(Q(name=name)  & Q(phone=phone) & Q(address=address) & Q(city=city)).exists():
            messages.warning(request, 'Le client existe déjà.')
        else:
            try:
                # Create and save the new customer
                Customer.objects.create(
                    name=name,
                    
                    phone=phone,
                    address=address,
                    city=city,
                    save_by=save_by
                )
                messages.success(request, 'Client ajouté avec succès.')
            except Exception as e:
                messages.error(request, f'Error adding customer: {e}')

        # Fetch all customers to display in the template
        customers = Customer.objects.all()
        return render(request, 'add_customer.html', {'customers': customers})
class AddInvoiceView(LoginRequiredMixin, View):
    template_name = 'add_invoice.html'

    def get(self, request, *args, **kwargs):
        customers = Customer.objects.select_related('save_by').all()
        articles = list(Article.objects.all().values('id', 'name', 'quantity', 'unit_price','prix'))

        # Convert Decimal to string
        unique_articles = {}
        for article in articles:
            article['unit_price'] = str(article['unit_price'])
            article['prix'] = str(article['prix'])
        context = {
            'customers': customers,
            'articles': articles,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        items = []
        customers = Customer.objects.select_related('save_by').all()
        articles = list(Article.objects.all().values('id', 'name', 'quantity', 'unit_price', 'prix'))

        # Convert Decimal to string
        for article in articles:
            article['unit_price'] = str(article['unit_price'])
            article['prix'] = str(article['prix'])
        context = {
            'customers': customers,
            'articles': articles,
        }
        try:
            customer = request.POST.get('customer')
            type = request.POST.get('invoice_type')

            article_ids = request.POST.getlist('article')
            qties = request.POST.getlist('qty')
            units = request.POST.getlist('unit')
            prixs = request.POST.getlist('prix')
            tvas = request.POST.getlist('tva')
            total_a = request.POST.getlist('total-a')
            total = request.POST.get('total')
            comment = request.POST.get('comment')

            total = Decimal(total)
            montant_ht = sum(Decimal(qty) * Decimal(unit) for qty, unit in zip(qties, units))
            montant_ttc = sum(Decimal(qty) * Decimal(unit) * (1 + Decimal(tva) / 100) for qty, unit, tva in zip(qties, units, tvas))

            invoice_object = {
                'customer_id': customer,
                'save_by': request.user,
                'total': total,
                'montant_ht': montant_ht,
                'montant_ttc': montant_ttc,
                'invoice_type': type,
                'comments': comment
            }

            invoice = Invoice.objects.create(**invoice_object)

            for index, article_id  in enumerate(article_ids):
                article = Article.objects.get(id=article_id)
                data = Article(
                    invoice=invoice,
                    name=article.name,
                    quantity=int(qties[index]),
                    unit_price=Decimal(units[index]),
                    tva=Decimal(tvas[index]),
                    total=Decimal(total_a[index]),
                    prix=Decimal(prixs[index]),
                    montant_ht=Decimal(qties[index]) * Decimal(units[index]),
                    montant_ttc=Decimal(qties[index]) * Decimal(units[index]) * (1 + Decimal(tvas[index]) / 100),
                )
                items.append(data)

            Article.objects.bulk_create(items)

            messages.success(request, "Données enregistrées avec succès.")

        except Exception as e:
            messages.error(request, f"Sorry, the following error has occurred: {e}")

        return render(request, self.template_name, {'customers': Customer.objects.all(), 'articles': Article.objects.values('name', 'unit_price')})

class InvoiceVisualizationView(LoginRequiredMixin, View):
    template_name = 'invoice.html'

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        context = get_invoice(pk)
        return render(request, self.template_name, context)


def get_invoice_pdf(request, *args, **kwargs):
    pk = kwargs.get('pk')
    context = get_invoice(pk)
    context['date'] = datetime.datetime.today()
    template = get_template('invoice-pdf.html')
    html = template.render(context)
    options = {
        'page-size': 'Letter',
        'encoding': 'UTF-8',
        "enable-local-file-access": ""
    }
    pdf = pdfkit.from_string(html, False, options)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = "attachment"
    return response



class AddInvoice2View(LoginRequiredMixin, View):
    """ add a new invoice view """

    template_name = 'add-invoice2.html'

    def get(self, request, *args, **kwargs):
        customers = Customer.objects.select_related('save_by').all()
        articles = list(Article.objects.all().values('id', 'name', 'quantity', 'unit_price'))
        
        # Convert Decimal to string
        for article in articles:
            article['unit_price'] = str(article['unit_price'])
        
        context = {
            'customers': customers,
            'articles': articles,
        }
        return render(request, self.template_name, context)

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        items = []

        customers = Customer.objects.select_related('save_by').all()
        articles = list(Article.objects.all().values('id', 'name', 'quantity', 'unit_price'))
        
        # Convert Decimal to string
        for article in articles:
            article['unit_price'] = str(article['unit_price'])

        context = {
            'customers': customers,
            'articles': articles,
        }

        try:
            customer = request.POST.get('customer')
            invoice_type = request.POST.get('invoice_type')
            
            article_names = request.POST.getlist('article')
            qties = request.POST.getlist('qty')
            units = request.POST.getlist('unit')
            total_a = request.POST.getlist('total-a')
            total = request.POST.get('total')
            comment = request.POST.get('comment')

            invoice_object = {
                'customer_id': customer,
                'save_by': request.user,
                'total': total,
                'invoice_type': invoice_type,
                'comments': comment
            }

            invoice2 = Invoice.objects.create(**invoice_object)

            for index, article_name in enumerate(article_names):
                data = Article(
                    invoice_id=invoice2.id,
                     
                    name=article_name,
                    quantity=qties[index],
                    unit_price=units[index],
                    total=total_a[index],
                )
                items.append(data)

            created = Article.objects.bulk_create(items)

            if created:
                messages.success(request, "Données enregistrées avec succès.")
            else:
                messages.error(request, "Désolé, veuillez réessayer, les données envoyées sont corrompues.")
        except Exception as e:
            messages.error(request, f"Sorry the following error has occurred: {e}.")

        return render(request, self.template_name, context)

        


class Invoice2VisualizationView(LoginRequiredMixin, View):
    """ This view helps to visualize the invoice """

    template_name = 'invoice2.html'

    def get(self, request, *args, **kwargs):

        pk = kwargs.get('pk')

        context = get_invoice(pk)

        return render(request, self.template_name, context)


def get_invoice2_pdf(request, *args, **kwargs):
    """ generate pdf file from html file """

    pk = kwargs.get('pk')

    context = get_invoice(pk)

    context['date'] = datetime.datetime.today()

    # get html file
    template = get_template('invoice2-pdf.html')

    # render html with context variables

    html = template.render(context)

    # options of pdf format 

    options = {
        'page-size': 'Letter',
        'encoding': 'UTF-8',
        "enable-local-file-access": ""
    }

    # generate pdf 

    pdf = pdfkit.from_string(html, False, options)

    response = HttpResponse(pdf, content_type='application/pdf')

    response['Content-Disposition'] = "attachement"

    return response



class AddInvoice3View(LoginRequiredMixin, View):
    template_name = 'add-invoice3.html'

    def get(self, request, *args, **kwargs):
        customers = Customer.objects.select_related('save_by').all()
        articles = Article.objects.all()
        
        # Remove duplicate articles based on the name
        unique_articles = {}
        for article in articles:
            if article.name not in unique_articles:
                unique_articles[article.name] = article
        
        context = {
            'customers': customers,
            'articles': unique_articles.values()
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        items = []

        try:
            codes = request.POST.getlist('code')
            article_names = request.POST.getlist('article')
            qties = request.POST.getlist('qty')
            units = request.POST.getlist('unit')
            total_a = request.POST.getlist('total-a')
            prix = request.POST.getlist('prix')  # Ensure this is retrieved correctly

            for code, name, qty, unit, total, price in zip(codes, article_names, qties, units, total_a, prix):  # Include 'prix' in the zip
                # Check if an article with the same code and name exists in the database
                existing_article = Article.objects.filter(code=code, name=name).exists()
                
                # Also check if an article with the same code and name is already in the items list
                if not existing_article and not any(item.code == int(code) and item.name == name for item in items):
                    data = Article(
                        code=int(code),
                        name=name,
                        quantity=int(qty),  # Ensure quantity is stored as an integer
                        unit_price=float(unit),  # Ensure unit_price is stored as a float
                        total=float(total),  # Ensure total is stored as a float
                        prix=float(price),  # Ensure prix is stored as a float
                    )
                    items.append(data)

            if items:
                created = Article.objects.bulk_create(items)
                if created:
                    messages.success(request, "Données enregistrées avec succès.")
                else:
                    messages.error(request, "Désolé, veuillez réessayer. Les données envoyées sont corrompues.")
            else:
                messages.warning(request, "Aucun nouvel article n'a été ajouté. Tous les articles fournis existent déjà.")

        except Exception as e:
            messages.error(request, f"Sorry, the following error has occurred: {e}.")

        # Update context to include articles for rendering the template after post
        customers = Customer.objects.select_related('save_by').all()
        articles = Article.objects.all()
        
        # Remove duplicate articles based on the name
        unique_articles = {}
        for article in articles:
            if article.name not in unique_articles:
                unique_articles[article.name] = article
        
        context = {
            'customers': customers,
            'articles': unique_articles.values()
        }

        return render(request, self.template_name, context)

class delete_article(View):
    def get(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        try:
            article.delete()
            messages.success(request, 'Article supprimé avec succès.')
        except Exception as e:
            messages.error(request, f'Error deleting article: {e}')
        return redirect('add-invoice3')
    
from django.shortcuts import render

def your_view(request):
    customers = Customer.objects.all()
    articles = Article.objects.all()  # Assuming you have an Article model
    return render(request, 'add-invoice2.html', {
        'customers': customers,
        'articles': articles,
    })