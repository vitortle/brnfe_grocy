from django.contrib import admin
from .models import Header, Item
from django import forms



class HeaderAdminForm(forms.ModelForm):
    class Meta:
        model = Header
        fields = ('access_key', 'purchase_date', 'place_name', 'city')

class HeaderAdmin(admin.ModelAdmin):
    form = HeaderAdminForm

    #inlines = [GradeInline,]
    #exclude = ('item',)
    verbose_name = ('Compra')
    list_display = ('access_key', 'purchase_date', 'place_name', 'city', ) #'cliente_limite', )
    # readonly_fields = ('nm_ab_cli',)
    fieldsets = (
        (None, {'fields':(
                          (('access_key', ),('purchase_date', 'place_name', 'city')))
                }),
    )
    #list_filter = ('nm_ab_cli',)
    search_fields = ['access_key', 'purchase_date', 'place_name', 'city']


class ItemAdminForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('item', 'gtin_code', 'description', 'purchase', 'liquid_price')

    """
    item
    product_code
    description
    qtty
    unit
    gross_price
    total_tax_value
    discount
    purchase
    liquid_price
    aditional_info
    gtin_code"""

class ItemAdmin(admin.ModelAdmin):
    form = ItemAdminForm

    #inlines = [GradeInline,]
    #exclude = ('item',)
    verbose_name = ('Item')
    list_display = ('item', 'gtin_code', 'description', 'purchase', 'liquid_price')
    # readonly_fields = ('nm_ab_cli',)
    fieldsets = (
        (None, {'fields':(
                          (('gtin_code', ),('description', 'liquid_price'), ('purchase')))
                }),
    )
    #list_filter = ('nm_ab_cli',)
    search_fields = ['gtin_code', 'description',]



# Register your models here.
admin.site.register(Header, HeaderAdmin)
admin.site.register(Item, ItemAdmin)