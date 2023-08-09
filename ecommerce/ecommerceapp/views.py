from django.shortcuts import render
from ecommerceapp.models import Contact, Product
from django.contrib import messages
from math import ceil

# Create your views here.

def index(request):
    allproducts = []
    catproduts = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catproduts}
    for cat in cats:
        product = Product.objects.filter(category=cat)
        n = len(product)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allproducts.append([product, range(1, nSlides), nSlides])
    context = {'allproducts' : allproducts}
    return render(request, 'index.html', context)

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        desc = request.POST.get('desc')
        pnumber = request.POST.get('pnumber')
        qry = Contact(name=name, email=email, desc=desc, phone=pnumber)
        qry.save()
        messages.success(request, "Succesfully Sent")
    return render(request, "contact.html")

def checkout(request):

    return render(request, "checkout.html")
