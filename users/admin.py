from django.contrib import admin
from .models import Payment
# Register your models here.

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """
    Админка для управления платежами пользователей.
    """
    list_display = ('id', 'user', 'amount', 'method', 'course', 'lesson', 'date')
    list_filter = ('method', 'course', 'lesson', 'user')
    search_fields = ('user__email',)
