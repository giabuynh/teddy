import json

import stripe
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from order.models import Order, OrderItem
from product.models import ProductSize

stripe.api_key = "sk_test_51JBAP1LGU0aggqknhAcsDpY9ezFV9xfSlLcXgRUcTzJZUU7ueOgyJCy4cUVzG4Dnpyv59eGa4OrdoD1zTXlTsITv00CTvKDjB8"


@api_view(['POST'])
def test_payment(request):
    test_payment_intent = stripe.PaymentIntent.create(
        amount=1000, currency='pln',
        payment_method_types=['card'],
        receipt_email='test@example.com'
    )
    return Response(status=status.HTTP_200_OK, data=test_payment_intent)


@api_view(['POST'])
def save_stripe_info(request):
    data = request.data
    email = data['email']
    card_info = {
        'number': data['card_number'],
        'exp_month': data['card_exp_month'],
        'exp_year': data['card_exp_year'],
        'cvc': data['card_cvc'],
    }
    extra_msg = ''

    customer_data = stripe.Customer.list(email=email).data
    payment_method_id = stripe.PaymentMethod.create(type='card', card=card_info)
    if len(customer_data) == 0:
        customer = stripe.Customer.create(
            email=email,
            payment_method=payment_method_id,
            invoice_settings={
                'default_payment_method': payment_method_id
            }
        )
    else:
        customer = customer_data[0]
        extra_msg += "Customer already existed.\n"

    prices = []
    for i in data['order_items']:
        # adding check existed
        price = stripe.Price.list(product=ProductSize.objects.get(id=i['product']).stripe_id)
        prices.append({"price": price.data[0]['id']})

    order = Order(customer_stripe=customer,)

    # payment = stripe.PaymentIntent.create(
    #     customer=customer,
    #     payment_method=payment_method_id,
    #     currency='vnd',
    #     amount=100000,
    #     # confirm=True
    # )

    # return Response(
    #     status=status.HTTP_200_OK,
    #     data={
    #         'message': 'Success',
    #         'data': {
    #             'customer_id': customer.id,
    #             'extra_msg': extra_msg,
    #             'payment': payment
    #         }
    #     })

    return Response(status=status.HTTP_200_OK, data='Test-Data')

# order{
#     id
#     charge_id,
#     customer_id
#     products: [
#         id,
#         quantity
#     ],
#     amount:
# }