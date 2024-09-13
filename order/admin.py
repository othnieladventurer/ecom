from django.contrib import admin
from .models import *

# Register your models here.


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'date_created']
    list_filter = ['status', 'date_created']
    search_fields = ['first_name', 'address']
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
