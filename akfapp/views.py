from django.shortcuts import render
from .models import Product
from math import ceil # Ex: ceil(7.3) = 8

# Create your views here.
def home(request):
    current_user = request.user
    print(current_user)
    allProud = []
    cat_id_Prod = Product.objects.values('category','id') # Ex: [{'category': 'C1', 'Product_id': 1},{'category': 'C2', 'Product_id': 2}
    cats_Prod = {item['category'] for item in cat_id_Prod} # we put it in {} to insure not repetition of category
    for cat in cats_Prod:
        prod = Product.objects.filter(category=cat)
        n=len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4)) # Ex: if n=11 than nSlides=3 that mean slide1=4 slide2=4 slide3=3
        allProud.append([prod,range(1,nSlides),nSlides])
    context = {'allProud':allProud}
    return render(request,'index.html',context)