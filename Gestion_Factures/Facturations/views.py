# myapp/views.py

from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout
from django.views.decorators.http import require_POST
import json

# product_manager/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Produit
from .forms import ProduitForm
from .models import Client
from .forms import ClientForm
from .models import Produit
from .models import Facturation
from .forms import FacturationForm
from .models import Client
from .forms import ClientSelectForm

def factureN_view(request, client_id, facture_id):
    client = get_object_or_404(Client, id=client_id)
    facturations = Facturation.objects.filter(client=client, facture_id=facture_id)
    
    context = {
        'client': client,
        'facturations': facturations,
        'facture_id': facture_id,
        'date_creation': facturations.first().date_creation if facturations.exists() else None,
    }
    return render(request, 'factureN.html', context)
#####################################################
def save_facturation(request):
    if request.method == 'POST':
        code_article = request.POST.get('code_article')
        quantite = int(request.POST.get('quantite'))
        remise = float(request.POST.get('remise'))
        tva = float(request.POST.get('tva'))

        # Assuming you have a method to retrieve Produit object based on code_article
        produit = get_produit_data(code_article)

        if produit:
            facturation = Facturation(produit=produit, quantite=quantite, remise=remise)
            facturation.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'message': 'Produit not found.'})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


def get_produit_data(request):
    if request.method == 'GET' and 'code_article' in request.GET:
        code_article = request.GET['code_article']
        produit = Produit.objects.filter(code_article=code_article).first()
        if produit:
            data = {
                'nom_produit': produit.nom_produit,
                'prix_unitaire': produit.prix_unitaire,
                'tva': produit.tva,
                # Add other fields as needed
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'Produit not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    ####################################

@csrf_exempt
@require_POST
def save_clients(request):
    if request.method == 'POST':
        clients_data = json.loads(request.POST.get('clients', '[]'))
        for client_data in clients_data:
            client_id = client_data.get('id')
            client_name = client_data.get('name')
            client_matricule = client_data.get('matricule')
            client_contact = client_data.get('contact')

            # Save the client data to the database
            Client.objects.update_or_create(
                id=client_id,
                defaults={
                    'nom_client': client_name,
                    'matricule_fiscale': client_matricule,
                    'contact': client_contact
                }
            )

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)
####################################
def factureN(request):
    # Display the facture with client and product details
    client_name = request.GET.get('client')
    client_matricule = request.GET.get('matricule')
    context = {
        'client_name': client_name,
        'client_matricule': client_matricule,
        # Add more context if needed
    }
    return render(request, 'factureN.html', context)

 #######################################  

def facturation_page(request):
    clients = Client.objects.all()
    facturations = Facturation.objects.all()
    client_form = ClientSelectForm()
    facturation_form = FacturationForm()

    if request.method == 'POST':
        client_form = ClientSelectForm(request.POST)
        facturation_form = FacturationForm(request.POST)

        if client_form.is_valid() and facturation_form.is_valid():
            client = client_form.cleaned_data['client']
            facturation = facturation_form.save(commit=False)
            facturation.client = client
            facturation.save()
            return redirect('facturation_page')

    context = {
        'clients': clients,
        'facturations': facturations,
        'client_form': client_form,
        'facturation_form': facturation_form,
    }
    return render(request, 'facturation_page.html', context)



####################################################
def ajouter_facturation(request):
    if request.method == 'POST':
        form = FacturationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('facturation_page')
    else:
        form = FacturationForm()
    return render(request, 'facturation_page.html', {'form': form})

def modifier_facturation(request, facturation_id):
    facturation = get_object_or_404(Facturation, pk=facturation_id)
    if request.method == 'POST':
        facturation_form = FacturationForm(request.POST, instance=facturation)
        if facturation_form.is_valid():
            facturation_form.save()
            return redirect('facturation_page')
    else:
        facturation_form = FacturationForm(instance=facturation)
    return render(request, 'modifier_facturation.html', {'facturation_form': facturation_form, 'facturation': facturation})

def supprimer_facturation(request, facturation_id):
    facturation = get_object_or_404(Facturation, pk=facturation_id)
    if request.method == 'POST':
        facturation.delete()
        return redirect('facturation_page')
    return render(request, 'supprimer_facturation.html', {'facturation': facturation})

######################################################################
def manage_clients(request):
    clients = Client.objects.all()
    form = ClientForm()
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_clients')
    return render(request, 'manage_clients.html', {'clients': clients, 'form': form})

def edit_client(request, pk):
    client = Client.objects.get(pk=pk)
    form = ClientForm(instance=client)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('manage_clients')
    return render(request, 'edit_client.html', {'form': form})

def delete_client(request, pk):
    client = Client.objects.get(pk=pk)
    if request.method == 'POST':
        client.delete()
        return redirect('manage_clients')
    return render(request, 'delete_client.html', {'client': client})

#####################################################################

def delete_produit(request, pk):
    produit = get_object_or_404(Produit, pk=pk)
    produit.delete()
    return redirect('manage_products')
    
def edit_produit(request, pk):
    produit = get_object_or_404(Produit, pk=pk)
    form = ProduitForm(instance=produit)

    if request.method == 'POST':
        form = ProduitForm(request.POST, instance=produit)
        if form.is_valid():
            form.save()
            return redirect('manage_products')

    return render(request, 'edit_produit.html', {'form': form})

def manage_products(request):
    produits = Produit.objects.all()
    form = ProduitForm()
    if request.method == 'POST':
        form = ProduitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_products')
    return render(request, 'manage_products.html', {'produits': produits, 'form': form})



#############################################

def products(request):
    return HttpResponse("Products Page")

def clients(request):
    return HttpResponse("Clients Page")

def invoice_history(request):
    return HttpResponse("Invoice History Page")

def bl_history(request):
    return HttpResponse("BL History Page")


###############################################

def home(request):
    return render(request, 'home.html')

def login(request):
    error_message = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == 'Yassine' and password == '2244':
            # Redirect to home page on successful login
             return render(request, 'home.html', {'username': username})
        else:
            error_message = 'Invalid username or password.'

    return render(request, 'login.html', {'error_message': error_message})

# Existing login and home views

def page_facture(request):
   return HttpResponse("page de facture")
def page_bon_livraison(request):
    return HttpResponse("page de bon livraison")



####################################
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout
# views.py


