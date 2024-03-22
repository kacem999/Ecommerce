from django.shortcuts import render, redirect
from .models import Product
from akfapp.models import Order
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from math import ceil  # Ex: ceil(7.3) = 8


# Create your views here.
def home(request):
    return render(request, 'index.html')


def purchase(request):
    current_user = request.user
    allProud = []
    query = request.GET.get('query')  # Get the search query
    if query:  # If a search query is present
        cat_id_Prod = Product.objects.filter(Product_name__icontains=query).values('category',
                                                                                   'id')  # Filter products based on the search query
    else:  # If no search query is present
        cat_id_Prod = Product.objects.values('category', 'id')
    cats_Prod = {item['category'] for item in cat_id_Prod}
    for cat in cats_Prod:
        if query:  # If a search query is present
            prod = Product.objects.filter(category=cat,
                                          Product_name__icontains=query)  # Filter products based on the search query
        else:  # If no search query is present
            prod = Product.objects.filter(category=cat)[:8]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProud.append([prod, range(1, nSlides), nSlides])
    categories = Product.objects.values('category').distinct()
    context = {'allProud': allProud, 'user': current_user, 'categories': categories}
    return render(request, 'purchase.html', context)


def category(request, category):
    current_user = request.user
    allProud = []
    products_list = Product.objects.filter(category=category)
    paginator = Paginator(products_list, 12)
    page_number = request.GET.get('page')  # Get the page number like ?page=2
    products = paginator.get_page(page_number)
    n = len(products)
    nSlides = n // 4 + ceil((n / 4) - (n // 4))
    allProud.append([products, range(1, nSlides), nSlides])
    context = {'allProud': allProud, 'user': current_user}
    return render(request, 'category.html', context)


def checkout(request):
    det = False
    if not request.user.is_authenticated:
        messages.warning(request, "Login & Try Again")
        return redirect('/auth/login')

    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amt')
        email = request.POST.get('email', '')
        address1 = request.POST.get('address1', '')
        address2 = request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        user = User.objects.get(username=email)
        order = Order.objects.create(Client=user, items_json=items_json, name=name, email=email, address1=address1,
                                     address2=address2, city=city, state=state, zip_code=zip_code, phone=phone,
                                     amount=amount)
        order.save()
        messages.success(request, "Order has been placed successfully")
        det = True
    if det is True:
        context = {'context': "delete"}
    else:
        context = {'context': "None"}
    return render(request, 'checkout.html', context)


def autocomplete(request):
    if 'term' in request.GET:
        term = request.GET['term']
        products_start_with_term = Product.objects.filter(Product_name__istartswith=term)
        products_contain_term = Product.objects.filter(Product_name__icontains=term).exclude(
            Product_name__istartswith=term)
        products = list(products_start_with_term) + list(products_contain_term)
        products = products[:5]
        product_list = [product.Product_name for product in products]
        return JsonResponse(product_list, safe=False)
    return render(request, 'purchase.html')
