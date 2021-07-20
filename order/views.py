import json
import stripe
from django.contrib.auth.models import AnonymousUser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, mixins, permissions, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from authentication.models import Account
from order.models import Order, OrderItem
from order.serializers import OrderSerializer
from product.models import Product, ProductSize


class OrderView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    # queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication = (JWTAuthentication,)

    def get_queryset(self):
        user = self.request.user.id
        if user is not AnonymousUser:
            return Order.objects.filter(customer=user)
        return None

    def get(self, request, *args, **kwargs):
        response = self.list(request, *args, **kwargs)
        for x in response.data:
            stripe_order = stripe.Order.retrieve(x['stripe_id'])
            x['total'] = stripe_order.amount
            x['status'] = stripe_order.status
        return response

    def post(self, request, *args, **kwargs):
        if not request.user.is_active:
           return "Inactive user"

        data = request.data
        customer = Account.objects.get(id=data['customer']) # should init name
        customer_name = customer.first_name + ' ' + customer.last_name
        items = []
        for i in data['items']:
            # improve: check if existed
            product = ProductSize.objects.get(id=i['product'])
            sku = stripe.SKU.list(product=product.stripe_id).data[0]
            items.append({
                'type': 'sku',
                'parent': sku['id'],
                'quantity': i['quantity']
            })
            # move to payment
            product.quantity -= i['quantity']
            product.save()

        order = stripe.Order.create(
            currency='vnd',
            items=items,
            shipping={
                'name': customer_name,
                'address': {
                    'line1': data['address'] # format this
                }
            }
        )

        request.POST._mutable = True
        request.data['stripe_id'] = order.id
        return self.create(request, *args, **kwargs)


class OrderDetailView(mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication = (JWTAuthentication,)

    def valid_order_customer(self):
        order_customer = Order.objects.get(id=self.kwargs['pk']).customer.id
        if str(self.request.user.id) == str(order_customer):
            return True
        return False

    def get(self, request, *args, **kwargs):
        if self.valid_order_customer():
            return self.retrieve(request, *args, **kwargs)
        return Response(data='No permission', status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        if self.valid_order_customer() and request.user.is_active:
            return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if self.valid_order_customer() and request.user.is_active:
            return self.destroy(request, *args, **kwargs)