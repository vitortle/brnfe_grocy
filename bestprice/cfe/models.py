from django.db import models

# Create your models here.
class Header(models.Model):
    cfeid = models.IntegerField()
    purchase_date = models.DateTimeField()
    place_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.purchase_date} - {self.place_name}"

class Item(models.Model):
    purchase = models.ForeignKey(Header, on_delete=models.CASCADE, related_name='items')
    item = models.IntegerField()
    product_code = models.CharField(max_length=20)
    description = models.CharField(max_length=50)
    qtty = models.FloatField()
    unit = models.CharField(max_length=10)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    tax = models.DecimalField(max_digits=6, decimal_places=2)
    total_price = models.DecimalField(max_digits=6, decimal_places=2)
    price_adjustment = models.CharField(max_length=20, null=True)
    adjustment_value = models.DecimalField(max_digits=6, decimal_places=2, default=0, null=True)

    def __str__(self):
        return f"{self.product_code} - {self.description}"