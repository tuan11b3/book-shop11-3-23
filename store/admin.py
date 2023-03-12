from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(DSDCKM)

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'happy', 'responded', 'staff_id')
    list_filter = ('responded', 'date',)
    search_fields = ('details',)

    class Meta:
        model = Feedback


admin.site.register(Feedback, FeedbackAdmin)
