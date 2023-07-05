from django.db import models

# Create your models here.
class Header(models.Model):
    cfeid = models.IntegerField()
    access_key = models.CharField(max_length=50)
    purchase_date = models.DateTimeField()
    place_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.purchase_date} - {self.place_name}"

class Item(models.Model):
    item = models.IntegerField()
    product_code = models.CharField(max_length=20)
    description = models.CharField(max_length=120)
    qtty = models.FloatField()
    unit = models.CharField(max_length=10)
    gross_price = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  
    total_tax_value = models.DecimalField(max_digits=10, decimal_places=5, default=0.00)  
    discount = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  
    liquid_price = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  
    aditional_info = models.TextField(blank=True, null=True)
    gtin_code = models.CharField(max_length=20, blank=True, null=True)
    ncm_code = models.CharField(max_length=10, blank=True, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=5, default=0.00)  
    calc_rule = models.CharField(max_length=1, blank=True, null=True)
    icms_value = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  
    pis_value = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  
    pis_st_value = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  
    cofins_value = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  
    confins_st_value = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  
    issqn_value = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  
    purchase = models.ForeignKey(Header, on_delete=models.CASCADE, related_name='items')
   
    def __str__(self):
        return f"{self.gtin_code} - {self.description}"
    
class Product(models.Model):
    gtin = models.CharField(max_length=20, blank=True, null=True)
    data = models.JSONField()

    def __str__(self):
        return self.gtin