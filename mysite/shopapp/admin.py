from csv import DictReader
from io import TextIOWrapper

from django.contrib import admin
from django.shortcuts import render, redirect
from django.urls import path

from shopapp.models import Product, Order
from shopapp.actions import mark_under_sanctions, mark_not_under_sanctions, mark_archived, mark_not_archived
from shopapp.forms import ImportCSVForm


class OrderInLine(admin.StackedInline):
    model = Order.products.through
    fk_name = 'product'


class ProductInLine(admin.StackedInline):
    model = Order.products.through
    fk_name = 'order'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    change_list_template = 'shopapp/change_list.html'

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

    def import_csv(self, request):
        if request.method == 'GET':
            form = ImportCSVForm
            context = {
                'form': form
            }
            return render(request, 'admin/csv_form.html', context=context)
        form = ImportCSVForm(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                'form': form
            }
            return render(request, 'admin/csv_form.html', context=context, status=400)
        csv_file = TextIOWrapper(
            form.files['csv_file'].file,
            encoding=request.encoding
        )
        reader = DictReader(csv_file)
        products = [Product(**product) for product in reader]
        Product.objects.bulk_create(products)
        return redirect('..')

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('import-csv', self.admin_site.admin_view(self.import_csv), name='import-csv')]
        return new_urls + urls


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

