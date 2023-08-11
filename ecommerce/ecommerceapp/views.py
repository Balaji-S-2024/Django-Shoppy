from django.shortcuts import render, redirect
from ecommerceapp.models import Contact, Product, Order, OrderUpdate
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
    if request.user.is_authenticated == False:
        messages.warning(request, "Login and Try Again")
        return redirect('/authent/login/')
    
    if request.method == 'POST':
        items_json = request.POST.get('itemsJson', '')
        amont = request.POST.get('amt')
        name = request.POST.get('name')
        email = request.POST.get('email')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        phone = request.POST.get('phone')
        zip_code = request.POST.get('zip_code')

        order = Order(
            items_json = items_json, 
            name = name, 
            amount = amont, 
            email = email, 
            address1 = address1, 
            address2 = address2,
            city = city, 
            state = state,
            zip_code = zip_code, 
            phone = phone, 
            )
        print(amont)
        Order.save()
        update = OrderUpdate(order_id = Order.order_id, update_desc = "The order is Placed! :)")
        update.save()
        thank = True


        # PayTm Integration
        id = Order.order_id
        oid=str(id)+"ShopyCart"
        param_dict = {

            'MID':keys.MID,
            'ORDER_ID': oid,
            'TXN_AMOUNT': str(amont),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/handlerequest/',

        }
        

        

    return render(request, "checkout.html")
