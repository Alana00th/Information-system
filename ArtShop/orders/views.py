from django.core.mail.backends import console
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from .models import *
from django.shortcuts import render
from .forms import CheckoutContactForm
from django.contrib.auth.models import User
from django.middleware.csrf import get_token



def basket_adding(request):
    csrf_token = get_token(request)
    return_dict = dict()
    session_key = request.session.session_key
    print (request.POST)
    data = request.POST
    product_id = data.get("product_id")
    nmb = data.get("nmb")
    is_delete = data.get("is_delete")
    if is_delete == 'true':
        ProductInBasket.objects.filter(id=product_id).update(is_active=False)
        # ProductInBasket.objects.filter(id=product_id).delete()
    else:
        new_product = ProductInBasket.objects.create(session_key=session_key, product_id=product_id,
                                                        is_active=True, nmb=nmb)

    products_in_basket = ProductInBasket.objects.filter(session_key=session_key,
                                                    is_active=True, order__isnull=True)
    products_total_nmb = products_in_basket.count()

    return_dict["products_total_nmb"] = products_total_nmb
    return_dict["products"] = list()

    for item in products_in_basket:
        product_dict = dict()
        product_dict["id"] = item.id
        product_dict["name"] = item.product.name
        product_dict["price_per_item"] = item.product.price
        product_dict["nmb"] = item.nmb
        return_dict["products"].append(product_dict)

    return JsonResponse(return_dict)
        #     new_product.nmb += int(nmb)
        #     new_product.save(force_update=True)
        #     return render(request, 'orders/checkout.html', locals())
        #common code for 2 cases

        # print(products_in_basket)

        # i = 0
        #


def checkout(request):

    session_key = request.session.session_key
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True, order__isnull=True)
    print (products_in_basket)
    for item in products_in_basket:
        print(item.order)


    form = CheckoutContactForm(request.POST or None)
    if request.POST:
        print(request.POST)
        if form.is_valid():
            print("yes")
            data = request.POST
            name = data.get("name", "3423453")
            phone = data["phone"]
            user, created = User.objects.get_or_create(username=phone, defaults={"first_name": name})

            order = Order.objects.create(user=user, customer_name=name, customer_phone=phone, status_id=1)

            for name, value in data.items():
                if name.startswith("product_in_basket_"):
                    product_in_basket_id = name.split("product_in_basket_")[1]
                    product_in_basket = ProductInBasket.objects.get(id=product_in_basket_id)
                    print(type(value))

                    product_in_basket.nmb = value
                    product_in_basket.order = order
                    product_in_basket.save(force_update=True)

                    ProductInOrder.objects.create(product=product_in_basket.product, nmb = product_in_basket.nmb,
                                                  price_per_item=product_in_basket.price_per_item,
                                                  total_price = product_in_basket.total_price,
                                                  order=order)


            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            print("no")
    return render(request, 'orders/checkout.html', locals())