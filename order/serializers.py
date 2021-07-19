from rest_framework import serializers
from order.models import Order, OrderItem
from product.models import Product


class OrderItemSerializer(serializers.ModelSerializer):
    # orderitem_set = serializers.CharField(max_length=100)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity']
        read_only_fields = ['id']

    def create(self, validated_data):
        items = [OrderItem(**x) for x in validated_data]
        return OrderItem.objects.bulk_create(items)


class OrderSerializer(serializers.ModelSerializer):
    # order_item_list = [OrderItem(), OrderItem()]
    items = OrderItemSerializer(many=True)

    def create(self, validated_data):
        temp_order_details = validated_data.pop('items')
        new_order = Order.objects.create(**validated_data)
        for i in temp_order_details:
            OrderItem.objects.create(**i, order=new_order)
        return new_order

    class Meta:
        model = Order
        fields = ['id', 'customer', 'stripe_id', 'address', 'date_created', 'stripe_payment_intent', 'items']
        read_only_fields = ['id', 'date_created',]
        list_serialize_class = OrderItemSerializer
