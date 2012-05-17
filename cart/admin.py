from django.contrib import admin
from models import Cart,Item

## Item (Inline)
class ItemInline(admin.TabularInline):
    model = Item

## Cart
class CartAdmin(admin.ModelAdmin):
    list_display = ('creation_date','checked_out',)
    list_filter=('checked_out',)
    inlines = [ItemInline]
admin.site.register(Cart,CartAdmin)
