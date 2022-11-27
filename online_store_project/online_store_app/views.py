from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .csv_interface import CSV_interface
from django.views.decorators.csrf import csrf_exempt
import requests as HTTP_Client
from requests_oauthlib import OAuth1
from dotenv import load_dotenv
import os

load_dotenv()

products_interface = CSV_interface('./online_store_app/data/products.csv')
shopping_cart_interface = CSV_interface('./online_store_app/data/shopping_cart.csv')

def index(request):
    data = products_interface.generate_product_categories

    all_products = products_interface.all_data
    if 'q' in request.GET:
        q = request.GET['q']
        for product in all_products:
            if q == product['name']:
                product_id = product['id']
                return HttpResponseRedirect(f'search/product/{product_id}/')
        return HttpResponseRedirect(f'search/not-found/{q}')
    return render(request, 'pages/index.html', {'categories':data})

def print_category_products(request, category):
    data = products_interface.get_products_by_category(category)
    return render(request, 'pages/category.html', {'category_products':data})

@csrf_exempt
def individual_product_details(request, product_id):
    data = products_interface.get_product_details(product_id)

    if request.method == 'POST':
        shopping_cart_data = shopping_cart_interface.append_one_row_to_file({'id':product_id, 'quantity':1})
        return HttpResponse('', {'cart':shopping_cart_data})
    return render(request, 'pages/individual_product.html', {'product':data})

def shopping_cart(request):
    existing_cart = shopping_cart_interface.all_data
    all_products = products_interface.all_data
    existing_cart_with_product_data = []

    for item in existing_cart:
        for product in all_products:
            if item['id'] == product['id']:
                if product not in existing_cart_with_product_data:
                    product['quantity'] = 1
                    existing_cart_with_product_data.append(product)
                else:
                    product['quantity'] += 1
    print(existing_cart_with_product_data)
    return render(request, 'pages/shopping_cart.html', {'cart':existing_cart_with_product_data})  

def not_in_stock(request, q):

    request.GET.get(q)

    auth = OAuth1(os.environ['apikey'], os.environ['secretkey'])
    endpoint = f"http://api.thenounproject.com/icon/{q}"

    API_response = HTTP_Client.get(endpoint, auth=auth)
    responseJSON = API_response.json()
    preview_url = responseJSON['icon']['preview_url']
    
    response = render(request,'pages/item_not_found.html', {'preview_url':preview_url})
    return response

