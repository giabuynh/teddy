import stripe
from django.contrib.auth.models import AnonymousUser
from django.http import JsonResponse
from django.urls import reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.utils import json
from authentication.models import Account
from order.models import Order
from product.models import ProductSize, Product

stripe.api_key = settings.STRIPE_SECRET_KEY


@api_view(['GET'])
def list_payments(request, *args, **kwargs):
    if request.user.id is None:
        return Response(status=status.HTTP_200_OK, data='Login first')

    email = Account.objects.get(id=request.user.id).email
    customer = stripe.Customer.list(email=email).data
    if len(customer):
        payments = stripe.PaymentIntent.list(customer=customer[0].id).data
        return Response(
            status=status.HTTP_200_OK,
            data=payments,
        )
    else:
        return Response(status=status.HTTP_200_OK, data='No PaymentIntent')


@api_view(['POST'])
def checkout(request, *args, **kwargs):
    if request.user.id is None:
        return Response(status=status.HTTP_200_OK, data='Login first')

    order = Order.objects.get(id=kwargs['pk'])
    if str(order.customer.id) != str(request.user.id):
        return Response(status=status.HTTP_200_OK, data='No permission')

    stripe_order = stripe.Order.retrieve(order.stripe_id)
    if stripe_order.status == 'paid':
        return Response(status=status.HTTP_200_OK, data='This order was paid')

    data = request.data
    card_info = {
        'number': data['card_number'],
        'exp_month': data['card_exp_month'],
        'exp_year': data['card_exp_year'],
        'cvc': data['card_cvc'],
    }
    extra_msg = ''

    email = Account.objects.get(id=order.customer.id).email

    # create a new customer
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

    payment = stripe.PaymentIntent.create(
        customer=customer,
        payment_method=payment_method_id,
        currency='vnd',
        amount=stripe_order.amount,
        confirm=True
    )

    order.stripe_payment_intent = payment.id
    order.save()
    # payment =
    stripe.Order.pay(stripe_order.id, source=data['card_token'], email=email)
    # stripe.Order.pay(stripe_order.id, customer=customer, email=email) # for active card

    return Response(
        status=status.HTTP_200_OK,
        data={
            'message': 'Success',
            'data': {
                'customer_id': customer.id,
                'extra_msg': extra_msg,
                'payment': payment,
            }
        })


@api_view(['GET'])
def payment_detail(request, *args, **kwargs):
    if request.user.id is None:
        return Response(status=status.HTTP_200_OK, data='Login first')

    order = Order.objects.get(id=kwargs['pk'])
    if str(order.customer.id) != str(request.user.id):
        return Response(status=status.HTTP_200_OK, data='No permission')

    if order.stripe_payment_intent == '':
        return Response(status=status.HTTP_200_OK, data='No payment information for this order')

    payment = stripe.PaymentIntent.retrieve(order.stripe_payment_intent)
    return Response(status=status.HTTP_200_OK, data=payment)
# class SuccessView(TemplateView):
#     template_name = 'success.html'
#
#
# class CancelView(TemplateView):
#     template_name = 'cancel.html'
#
#
# class ProductLandingPageView(TemplateView):
#     template_name = 'landing.html'
#
#     def get_context_data(self, **kwargs):
#         product = ProductSize.objects.get(id='5ac711a4-1fb9-488a-9e32-3f64b8fdba62')
#         context = super(ProductLandingPageView, self).get_context_data(**kwargs)
#         context.update({
#             'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
#             'product': product,
#         })
#     return context


# class CheckoutSessionView(View):
#     def post(self, request, *args, **kwargs):
#         product_id = self.kwargs["pk"]
#         product = ProductSize.objects.get(id=product_id)
#
#         DOMAIN = "http://127.0.0.1:8000"
#         checkout_session = stripe.checkout.Session.create(
#             payment_method_types=['card'],
#             line_items=[
#                 {
#                     'price_data': {
#                         'currency': 'vnd',
#                         'unit_amount': product.price,
#                         'product_data': {
#                             'name': product.name,
#                             # 'images': ['https://i.imgur.com/EHyR2nP.png'],
#                         },
#                     },
#                     'quantity': 1,
#                 },
#             ],
#             metadata={
#                 "product_id": product.id
#             },
#             mode='payment',
#             success_url = DOMAIN + '/success/',
#             cancel_url = DOMAIN + '/cancel/',
#         )
#         return JsonResponse({
#             'id': checkout_session.id
#         })

# @csrf_exempt
# def create_checkout_session(request, id):
#     request_data = json.loads(request.body)
#     product = get_object_or_404(Product, pk=id)
#
#     stripe.api_key = settings.STRIPE_SECRET_KEY
#     checkout_session = stripe.checkout.Session.create(
#         # Customer Email is optional,
#         # It is not safe to accept email directly from the client side
#         customer_email = request_data['email'],
#         payment_method_types=['card'],
#         line_items=[
#             {
#                 'price_data': {
#                     'currency': 'usd',
#                     'product_data': {
#                     'name': product.name,
#                     },
#                     'unit_amount': int(product.price * 100),
#                 },
#                 'quantity': 1,
#             }
#         ],
#         mode='payment',
#         success_url=request.build_absolute_uri(
#             reverse('success')
#         ) + "?session_id={CHECKOUT_SESSION_ID}",
#         cancel_url=request.build_absolute_uri(reverse('failed')),
#     )
#
#     # OrderDetail.objects.create(
#     #     customer_email=email,
#     #     product=product, ......
#     # )
#
#     order = OrderDetail()
#     order.customer_email = request_data['email']
#     order.product = product
#     order.stripe_payment_intent = checkout_session['payment_intent']
#     order.amount = int(product.price * 100)
#     order.save()
#
#     # return JsonResponse({'data': checkout_session})
#     return JsonResponse({'sessionId': checkout_session.id})
