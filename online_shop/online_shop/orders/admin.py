from django.contrib import admin
from .models import Order, OrderItem


# using ModelInline to include it as an inline in the OrderAdmin
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'paid', 'created', 'updated')
    list_filter = ('paid', 'created', 'updated')
    inlines = [OrderItemInline,]
