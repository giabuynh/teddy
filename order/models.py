import uuid
from django.db import models
from authentication.models import Account
from product.models import ProductSize


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    customer = models.ForeignKey(Account, on_delete=models.PROTECT)
    stripe_id = models.CharField(max_length=200, blank=True)
    stripe_payment_intent = models.CharField(max_length=200, blank=True)
    address = models.CharField(max_length=100)
    # status = models.CharField(max_length=50, choices=STATUS, default='Pending')
    date_created = models.DateTimeField(auto_now_add=True, blank=False)
    # items = models.ManyToManyField(OrderItem)

    class Meta:
        verbose_name_plural = 'Orders'

    def __str__(self):
        return self.customer.username + " " + str(self.date_created)

    # def get_total(self):
    #     order_items = self.items.values('id')
    #     total = 0
    #     for x in order_items:
    #         total += OrderItem.objects.get(id=x['id']).get_items_price()
    #     return total


class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, to_field='id', related_name='items')
    product = models.ForeignKey(ProductSize, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=False, default=1)

    class Meta:
        verbose_name_plural = 'OrderItems'
        unique_together = (('order', 'product'),)

    def __str__(self):
        return str(self.product) + ' ' + str(self.quantity)

    def get_items_price(self):
        return self.quantity * self.product.price