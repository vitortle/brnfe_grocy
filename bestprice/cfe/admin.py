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
    verbose_name = ('Header')
    list_display = ('access_key', 'purchase_date', 'place_name', 'city', ) #'cliente_limite', )
    # readonly_fields = ('nm_ab_cli',)
    fieldsets = (
        (None, {'fields':(
                          (('access_key', ),('purchase_date', 'place_name', 'city')))
                }),
    )
    #list_filter = ('nm_ab_cli',)
    search_fields = ['access_key', 'purchase_date', 'place_name', 'city']

# Register your models here.
admin.site.register(Header, HeaderAdmin)
admin.site.register(Item)