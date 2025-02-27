from django.contrib import admin
from shopapp.models import Product, Order
from shopapp.actions import mark_under_sanctions, mark_not_under_sanctions, mark_archived, mark_not_archived


class OrderInLine(admin.StackedInline):
    model = Order.products.through
    fk_name = 'product'


class ProductInLine(admin.StackedInline):
    model = Order.products.through
    fk_name = 'order'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'price', 'being_under_sanctions')
    search_fields = ('name', 'price')
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description'),
        }
         ),
        ('Дополнительно', {
            'fields': ('price', 'being_under_sanctions'),
        }
         ),
    )
    inlines = [OrderInLine]
    actions = [mark_under_sanctions, mark_not_under_sanctions, 'deleted_selected']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'address', 'promocode', 'user', 'is_archived')
    search_fields = ('promocode', 'user')
    fieldsets = (
        ('Основная информация', {
            'fields': ('address', 'user'),
        }
         ),
        ('Дополнительно', {
            'fields': ('promocode', 'is_archived'),
        }
         ),
    )
    inlines = [ProductInLine]
    actions = [mark_archived, mark_not_archived]

